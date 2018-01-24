#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output classes for ETL with SensorThings API.
#
# Author: Just van den Broecke
#

from os import path
import requests
import json
import base64

from stetl.util import Util
from stetl.packet import FORMAT
from stetl.component import Config
from stetl.outputs.httpoutput import HttpOutput

log = Util.get_log('staoutput')


class STAOutput(HttpOutput):
    """
    Output via SensorThings API (STA) over plain HTTP using the HttpOutput base class.
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

    @Config(ptype=str, default=None, required=False)
    def template_file_root(self):
        """
        STA template file root: where STA request template-files are stored.

        Required: False

        Default: statemplates relative to file's dir
        """
        pass

    def __init__(self, configdict, section):
        HttpOutput.__init__(self, configdict, section, consumes=FORMAT.record_array)

        if self.template_file_root is None:
            self.template_file_root = path.join(path.dirname(path.realpath(__file__)), 'statemplates')

        # Template file, to be used as POST body with substituted values
        # TODO use Jinja2 formatting i.s.o. basic string formatting
        self.entities_list = ['thing', 'location', 'datastream', 'observation', 'observedproperty', 'sensor']
        self.entity_templates = {}
        self.sensors = {}
        self.things = {}
        self.locations = {}
        self.observedproperties = {}

        self.base_path = self.path
        self.base_url = 'http://%s:%d%s' % (self.host, self.port, self.path)

        self.http_session = requests.Session()

    # generic util to format Python datetime object to STA format date
    # Time format: "yyyy-MM-dd'T'HH:mm+0N00"  e.g. 2013-09-29T18:46:19+0100
    def format_datetime(self, dt):
        t_offset = dt.tzinfo._offset.seconds / 3600
        return dt.strftime('%Y-%m-%dT%H:%M:%S' + '+0%d:00' % t_offset)

    # generic util to read/GET from STA
    def read_from_url(self, url, parameters=None):
        """
        Read the data from the URL.
        :param url: the url to fetch
        :param parameters: optional dict of query parameters
        :return:
        """
        log.info('Fetch data from URL: %s ...' % url)

        headers = {
            "Content-Type": self.content_type,
            "Accept": self.content_type
        }
        json_response = None

        try:
            r = self.http_session.get(url, params=parameters, headers=headers)
            json_response = r.json()
        except Exception as e:
            log.error('Error fetching from URL %s: e=%s' % (url, str(e)))

        # everything is fine
        return json_response

    def post_to_url(self, payload):
        self.req_nr += 1

        headers = {
            "Host": self.host,
            "User-Agent": "Stetl Python http",
            "Content-Type": self.content_type,
            # "Accept", self.accept_type,
            "Content-Length": "%d" % len(payload)
        }

        # basic auth: http://mozgovipc.blogspot.nl/2012/06/python-http-basic-authentication-with.html
        # base64 encode the username and password
        # write the Authorization header like: 'Basic base64encode(username + ':' + password)
        # TODO use Requests Session
        status_code = 0
        status_msg = ''
        response_text = ''
        url = self.base_url + self.path
        if self.user is not None:
            auth = base64.encodestring('%s:%s' % (self.user, self.password)).replace('\n', '')
            headers["Authorization"] = "Basic %s" % auth

        log.info('POST to URL: %s ...' % url)

        try:
            r = self.http_session.post(url, data=payload, headers=headers)
            response_text = r.text
            status_code = r.status_code
            status_msg = str(r.status_code)
            headers = r.headers
        except Exception as e:
            log.error('Error posting to URL %s: e=%s' % (url, str(e)))

        log.info("Req nr %d - response status: code=%d msg=%s" % (self.req_nr, status_code, status_msg))

        if status_code == 200:
            pass
        elif status_code == 204:
            response_text = ''
        else:
            log.info("Response Headers: %s" % str(headers))
            # log.info('Content: %s' % response_text)

        return status_code, status_msg, response_text

    def patch(self, entity_type, entity_id, json_struct):
        log.info('PATCH: entity type=%s id=%s' % (entity_type, entity_id))
        url = self.base_url + "/" + entity_type + "(%d)" % entity_id
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        if self.user is not None:
            auth = base64.encodestring('%s:%s' % (self.user, self.password)).replace('\n', '')
            headers["Authorization"] = "Basic %s" % auth

        status_code = -1
        status_msg = ''
        response_text = ''
        try:
            response = self.http_session.patch(url, data=json.dumps(json_struct), headers=headers)
            status_code = response.status_code
            status_msg = str(response.status_code)
            response_text = response.content
            log.info('PATCH: status=%s' % response_text)
        except Exception as e:
            log.error('Error PATCHing to URL %s: e=%s' % (url, str(e)))
            pass

        return status_code, status_msg, response_text

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

            # store the Thing's named-datastreams internally in object
            thing['datastreams'] = {}
            self.things[id] = thing

    # called by baseclass, overloaded
    def init(self):
        # Init the templates used for POSTing to STA
        self.init_templates()

        # Init local STA Entity collections for reference
        # self.init_things()
        self.init_observedproperties()
        self.init_sensors()

    # called by baseclass, overloaded
    def exit(self):
        """
        Mainly patch all Things with their last update time.
        """
        for device_id in self.things:
            thing = self.things[device_id]
            if 'last_update' not in thing['properties'] or \
                    'device_meta' not in thing['properties']:
                continue

            # update (patch) Thing last update time once per session
            thing_patch = {
                "properties": {
                    "id": device_id,
                    "project_id": int(device_id) / 10000,
                    "device_meta": thing['properties']['device_meta'],
                    "last_update": thing['properties']['last_update']
                }
            }
            status_code, status_msg, response_text = self.patch('Things', thing['@iot.id'], thing_patch)

            # Check result
            if status_code in [200, 201]:
                log.info('YES patched Thing! device_id=%s status=%s' % (device_id, status_msg))
            else:
                log.warn('FAIL patching Thing! device_id=%s status=%s resp=%s' % (device_id, status_msg, response_text))

    def post_sensor(self, record):
        format_args = dict()

        format_args['name'] = record['name']
        format_args['sensor_meta'] = record['sensor_meta']

        # Create POST payload from template
        payload = self.entity_templates['sensor'].format(**format_args)

        # HttpOutput needs self.path, this changes per REST call
        self.path = '/Sensors'

        # Do the STA POST and return JSON object
        statuscode, statusmessage, res = self.post_to_url(payload)
        entity = json.loads(res)
        return entity

    def post_observedproperty(self, record):
        format_args = dict()

        format_args['name'] = record['name']
        format_args['unit'] = record['unit']

        # Create POST payload from template
        payload = self.entity_templates['observedproperty'].format(**format_args)

        # HttpOutput needs self.path, this changes per REST call
        self.path = '/ObservedProperties'

        # Do the STA POST and return JSON object
        statuscode, statusmessage, res = self.post_to_url(payload)
        entity = json.loads(res)
        return entity

    def post_thing(self, record, location):

        format_args = dict()

        format_args['station_id'] = record['device_id']
        format_args['project_id'] = int(record['device_id'] / 10000)
        format_args['last_update'] = self.format_datetime(record['time'])
        format_args['device_meta'] = record['device_meta']
        # format_args['station_altitude'] = record['altitude']
        format_args['station_lon'] = record['lon']
        format_args['station_lat'] = record['lat']
        format_args['location_id'] = location['@iot.id']
        # format_args['historical_locations_link'] = location['HistoricalLocations@iot.navigationLink']

        # Create POST payload from template
        payload = self.entity_templates['thing'].format(**format_args)
        log.info('POST Thing - Payload: %s' % str(payload))

        # HttpOutput needs self.path, this changes per REST call
        self.path = '/Things'

        # Do the STA POST and return JSON object
        statuscode, statusmessage, res = self.post_to_url(payload)
        thing = json.loads(res)
        return thing

    def post_location(self, record):
        format_args = dict()

        format_args['station_id'] = record['device_id']
        format_args['lon'] = record['lon']
        format_args['lat'] = record['lat']

        # Create POST payload from template
        payload = self.entity_templates['location'].format(**format_args)
        log.info('POST Location - Payload: %s' % str(payload))

        # HttpOutput needs self.path, this changes per REST call
        self.path = '/Locations'

        # Do the STA POST and return JSON object
        statuscode, statusmessage, res = self.post_to_url(payload)
        entity = json.loads(res)
        return entity

    def post_datastream(self, thing, record):
        # {'device_id': 1, 'name': 'temperature', 'value': 19, 'unit': 'Celsius', 'gid': 50,
        # 'time': datetime.datetime(2016, 4, 27, 5, 0, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=120, name=None)),
        # 'lat': 51.472585, , 'lon': 5.671208, , 'altitude': 210, }
        format_args = dict()
        name = record['name']

        format_args['thing_id'] = thing['@iot.id']

        # Add sensor to local collection if not existing for name
        sensor = self.sensors.get(name)
        if not sensor:
            sensor = self.post_sensor(record)
            self.sensors[name] = sensor
        format_args['sensor_id'] = sensor['@iot.id']

        # Add observedproperty to local collection if not existing for name
        observedproperty = self.observedproperties.get(name)
        if not observedproperty:
            observedproperty = self.post_observedproperty(record)
            self.observedproperties[name] = observedproperty

        format_args['observedproperty_id'] = observedproperty['@iot.id']
        format_args['station_id'] = record['device_id']
        format_args['name'] = record['name']
        format_args['label'] = record['label']
        format_args['unit'] = record['unit']

        # Create POST payload from template
        payload = self.entity_templates['datastream'].format(**format_args)

        # HttpOutput needs self.path, this changes per REST call
        self.path = '/Datastreams'

        # Do the STA POST and return JSON object
        statuscode, statusmessage, res = self.post_to_url(payload)
        datastream = json.loads(res)
        return datastream

    # Called by HttpOutput base class before post(), overridden
    def create_payload(self, packet):
        record = packet.data
        device_id = str(record['device_id'])
        ds_name = record['name']

        thing = self.things.get(device_id)
        if not thing:
            # Not in local collection: try fetch from server
            params = {"$filter": "name eq '%s'" % device_id, "$expand": 'Locations'}
            th_resp = self.read_from_url(self.base_url + '/Things', params)
            if 'error' in th_resp or 'value' not in th_resp:
                log.error('Error response fetching Thing for device id %s: rsp=%s' % (device_id, str(th_resp)))
                return None

            th_list = th_resp['value']
            for th in th_list:
                th_name_n = th['name']
                th['datastreams'] = {}
                self.things[th_name_n] = th

                # update location once per session
                location_patch = {
                    "location": {
                        "coordinates": [record['lon'], record['lat']],
                        "type": "Point"
                    }
                }
                location_id = th['Locations'][0]['@iot.id']
                self.patch('Locations', location_id, location_patch)

            thing = self.things.get(device_id)

            if not thing:
                # Not on server : post new and add
                location = self.post_location(record)
                self.locations[device_id] = location
                thing = self.post_thing(record, location)
                thing['datastreams'] = {}
                self.things[device_id] = thing

        datastream = thing['datastreams'].get(ds_name)
        if not datastream:
            # Try to get DS for Obs Prop for this Thing
            ds_resp = self.read_from_url(
                self.base_url + '/Things(%d)/Datastreams?$expand=ObservedProperty' % thing['@iot.id'])

            if 'error' not in ds_resp:
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
        format_args['sample_time'] = self.format_datetime(record['time'])
        format_args['sample_value'] = record['value']
        format_args['datastream_id'] = datastream['@iot.id']
        format_args[
            'parameters'] = '"gid": %d, "raw_gid": %d, "station": %d, "device_meta": "%s", "sensor_meta": "%s", "name": "%s"' % (
            record['gid'], record['gid_raw'], record['device_id'], record['device_meta'], record['sensor_meta'],
            record['name'])

        # Create POST payload from template
        payload = self.entity_templates['observation'].format(**format_args)

        # Update last update and device_meta time property for Thing from Observation
        thing['properties']['last_update'] = format_args['sample_time']
        thing['properties']['device_meta'] = record['device_meta']

        # REST: post to remote collection
        self.path = '/Observations'

        return payload

    # Called by HttpOutput base class after create_payload(), overridden
    def post(self, packet, payload):
        # Typical data record:
        # {'device_id': 1, 'name': 'temperature', 'value': 19, 'unit': 'Celsius', 'gid': 50,
        # 'time': datetime.datetime(2016, 4, 27, 5, 0, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=120, name=None)),
        # 'lat': 51.472585, , 'lon': 5.671208, , 'altitude': 210, }
        record = packet.data
        component = record['name']
        device_id = str(record['device_id'])
        gid = record['gid']
        id = '%s-%s-%s' % (device_id, component, gid)

        log.info('====START POST Observation id=%s' % id)

        statuscode, statusmessage, res = self.post_to_url(payload)

        # Check result
        if statuscode in [200, 201]:
            log.info('YES added Observation! id=%s status=%s' % (id, statusmessage))
        else:
            log.warn('FAIL POST Observation status=%d payload=%s res=%s' % (statuscode, payload, res))

        log.info('====END POST Observation id=%s' % id)

        return statuscode, statusmessage, res
