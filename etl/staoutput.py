#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output classes for ETL with SensorThings API.
#
# Author: Just van den Broecke
#
from os import sys, path
from stetl.outputs.httpoutput import HttpOutput
from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import json
from sensordefs import *

from stetl.util import Util
from stetl.packet import FORMAT
from stetl.component import Config
log = Util.get_log('staoutput')

class STAOutput(HttpOutput):
    """
    Output via SensorThings API (STA) over plain HTTP.
    See examples: http://www.sensorup.com/docs/?python

    consumes=FORMAT.record_array
    """

    @Config(ptype=str, default='application/json;charset=UTF-8', required=False)
    def content_type(self):
        """
        The content type (for template).

        Required: True

        Default: application/json;charset=UTF-8
        """
        pass

    @Config(ptype=str, default='statemplates', required=False)
    def template_file_root(self):
        """
        SOS template file root: where SOS request and procedure template-files are stored.

        Required: False

        Default: sostemplates
        """
        pass

    def __init__(self, configdict, section):
        HttpOutput.__init__(self, configdict, section, consumes=FORMAT.record_array)

        # Template file, to be used as POST body with substituted values
        # TODO use Jinja2 formatting i.s.o. basic string formatting
        self.entities_list = ['thing', 'datastream', 'observation', 'observedproperty', 'sensor']
        self.entity_templates = {}
        self.sensors = {}
        self.things = {}
        self.observedproperties = {}

        self.base_path = self.path
        self.base_url = 'http://%s:%d%s' % (self.host, self.port, self.path)

    def init_templates(self):
        # read all POST payload templates once
        for entity in self.entities_list:
            entity_templ_path = '%s/%s.json' % (self.template_file_root, entity)
            log.info('Init: read template file for: %s from %s' % (entity, entity_templ_path))
            with open(entity_templ_path, 'r') as f:
                self.entity_templates[entity] = f.read()

    def init_sensors(self):
        log.info('Init: read all Sensors')

        rsp = self.read_from_url(self.base_url + '/Sensors')
        entity_list = rsp['value']
        for entity in entity_list:
            # id = entity['name']
            try:
                id = entity['metadata']
                self.sensors[id] = entity
            except:
                pass

    def init_observedproperties(self):
        log.info('Init: read all ObservedProperties')

        rsp = self.read_from_url(self.base_url + '/ObservedProperties')
        entity_list = rsp['value']
        for entity in entity_list:
            id = entity['name']
            self.observedproperties[id] = entity

    def init_things(self):
        log.info('Init: read all Things')

        things_rsp = self.read_from_url(self.base_url + '/Things')
        self.things_list = things_rsp['value']
        for thing in self.things_list:
            id = thing['properties']['id']
            thing['datastreams'] = {}
            self.things[id] = thing

    def init(self):
        self.init_templates()
        self.init_things()
        self.init_observedproperties()
        self.init_sensors()

    def post_sensor(self, record):
        format_args = dict()

        format_args['name'] = record['name']
        format_args['label'] = record['unit']

        payload = self.entity_templates['sensor'].format(**format_args)
        self.path = self.base_path + '/Sensors'
        statuscode, statusmessage, res = HttpOutput.post(self, None, payload)
        entity = json.loads(res)
        return entity

    def post_observedproperty(self, record):
        format_args = dict()

        format_args['name'] = record['name']
        format_args['unit'] = record['unit']

        payload = self.entity_templates['observedproperty'].format(**format_args)
        self.path = self.base_path + '/ObservedProperties'
        statuscode, statusmessage, res = HttpOutput.post(self, None, payload)
        entity = json.loads(res)
        return entity

    def post_thing(self, record):
        format_args = dict()

        format_args['station_id'] = record['device_id']
        # format_args['station_altitude'] = record['altitude']
        format_args['station_lon'] = record['lon']
        format_args['station_lat'] = record['lat']

        payload = self.entity_templates['thing'].format(**format_args)
        self.path = self.base_path + '/Things'
        statuscode, statusmessage, res = HttpOutput.post(self, None, payload)
        thing = json.loads(res)
        return thing

    def post_datastream(self, thing, record):
        # {'device_id': 1, 'name': 'temperature', 'value': 19, 'unit': 'Celsius', 'gid': 50,
        # 'time': datetime.datetime(2016, 4, 27, 5, 0, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=120, name=None)),
        # 'lat': 51.472585, , 'lon': 5.671208, , 'altitude': 210, }
        format_args = dict()
        name = record['name']
        sensor_def = SENSOR_DEFS[name]

        format_args['thing_id'] = thing['@iot.id']

        # Add sensor is not exists for name
        sensor = self.sensors.get(name)
        if not sensor:
            sensor = self.post_sensor(record)
            self.sensors[name] = sensor
        format_args['sensor_id'] = sensor['@iot.id']

        # Add observedproperty is not exists for name
        observedproperty = self.observedproperties.get(name)
        if not observedproperty:
            observedproperty = self.post_observedproperty(record)
            self.observedproperties[name] = observedproperty

        format_args['observedproperty_id'] = observedproperty['@iot.id']
        format_args['station_id'] = record['device_id']
        format_args['name'] = record['name']
        format_args['label'] = sensor_def['label']
        format_args['unit'] = record['unit']

        payload = self.entity_templates['datastream'].format(**format_args)
        self.path = self.base_path + '/Datastreams'
        statuscode, statusmessage, res = HttpOutput.post(self, None, payload)
        datastream = json.loads(res)
        return datastream

    def read_from_url(self, url, parameters=None):
        """
        Read the data from the URL.
        :param url: the url to fetch
        :param parameters: optional dict of query parameters
        :return:
        """
        # log.info('Fetch data from URL: %s ...' % url)
        req = Request(url)
        req.add_header('Content-Type', self.content_type)
        req.add_header('Accept', self.content_type)
        json_response = None
        try:
            # Urlencode optional parameters
            query_string = None
            if parameters:
                query_string = urllib.urlencode(parameters)

            response = urlopen(req, query_string)
            response_str = response.read()
            json_response = json.loads(response_str)
        except HTTPError as e:
            log.error('HTTPError fetching from URL %s: code=%d e=%s' % (url, e.code, e))
        except URLError as e:
            log.error('URLError fetching from URL %s: reason=%s e=%s' % (url, e.reason, e))

        # everything is fine
        return json_response

    def post(self, packet, payload):
        # {'device_id': 1, 'name': 'temperature', 'value': 19, 'unit': 'Celsius', 'gid': 50,
        # 'time': datetime.datetime(2016, 4, 27, 5, 0, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=120, name=None)),
        # 'lat': 51.472585, , 'lon': 5.671208, , 'altitude': 210, }
        record = packet.data
        component = record['name']
        device_id = str(record['device_id'])
        gid = record['gid']
        id = '%s-%s-%s' % (device_id, component, gid)

        log.info('====START POST Observation id=%s' % id)

        statuscode, statusmessage, res = HttpOutput.post(self, packet, payload)

        # Check result
        if statuscode in [200, 201]:
            log.info('YES added Observation! id=%s status=%s' % (id, statusmessage))
        else:
            log.warn('FAIL POST Observation status=%d payload=%s res=%s' % (statuscode, payload, res))

        log.info('====END POST Observation id=%s' % id)

        return statuscode, statusmessage, res

    def create_payload(self, packet):
        record = packet.data
        device_id = str(record['device_id'])
        thing = self.things.get(device_id)
        ds_name = record['name']
        if not thing:
            thing = self.post_thing(record)
            thing['datastreams'] = {}
            datastream = self.post_datastream(thing, record)
            thing['datastreams'][ds_name] = datastream
            self.things[device_id] = thing

        datastream = thing['datastreams'].get(ds_name)
        if not datastream:
            ds_resp = self.read_from_url(self.base_url + '/Things(%d)/Datastreams?$expand=ObservedProperty' % thing['@iot.id'])
            ds_list = ds_resp['value']
            for ds in ds_list:
                ds_name_n = ds['ObservedProperty']['name']
                thing['datastreams'][ds_name_n] = ds

            datastream = thing['datastreams'].get(ds_name)
            if not datastream:
                datastream = self.post_datastream(thing, record)
                thing['datastreams'][ds_name] = datastream

        format_args = dict()

        # Time format: "yyyy-MM-dd'T'HH:mm+0N00"  e.g. 2013-09-29T18:46:19+0100
        t = record['time']
        t_offset = t.tzinfo._offset.seconds / 3600
        format_args['sample_time'] = t.strftime('%Y-%m-%dT%H:%M:%S' + '+0%d00' % t_offset)
        format_args['sample_value'] = record['value']
        format_args['datastream_id'] = datastream['@iot.id']
        format_args['details'] = 'gid=%d, raw_gid=%d, station=%d, name=%s' % (record['gid'], record['gid_raw'], record['device_id'], record['name'])

        payload = self.entity_templates['observation'].format(**format_args)

        # REST: post to collection
        self.path = self.base_path + '/Observations'

        return payload