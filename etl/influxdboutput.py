#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output classes for ETL: write record_array to InfluxDB database server via HTTP.
#
# Author: Just van den Broecke
#
import time
import calendar
import Geohash

from stetl.outputs.httpoutput import HttpOutput
from stetl.util import Util
from stetl.packet import FORMAT
from stetl.component import Config

log = Util.get_log('influxdboutput')

class InfluxDbOutput(HttpOutput):
    """
    Output via InfluxDB protocol over plain HTTP.

    consumes=FORMAT.record_array

    Config example:
    # Write records to remote InfluxDB server
    [output_influxdb_write]
    class = influxdboutput.InfluxDbOutput
    input_format = record_array
    method = POST
    list_fanout = False
    content_type = application/x-www-form-urlencoded
    host = test.smartemission.nl
    port = 8086
    database = smartemission
    measurement = joseraw
    tags_map = {{'station': 'device_id', 'component': 'name' }}
    geohash_wkt_attr = point
    fields_map = {{'value': 'value'}}
    time_attr = time
    user = theuser
    password = thepass

    """

    @Config(ptype=str, required=True)
    def database(self):
        """
        The "database" is a db-like entity in an InfluxDB database

        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=str, required=True)
    def measurement(self):
        """
        The required "measurement" is a table-like entity in an InfluxDB database

        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=dict, default=None, required=False)
    def tags_map(self):
        """
        The optional tag keys, sort of free-to-choose columns with their mappings to attributes in incoming records.
        Example: {'station': 'device_id', 'component': 'name' }
        Required: True

        Default: None
        """
        pass

    @Config(ptype=dict, required=True)
    def fields_map(self):
        """
        The actual value fields with their mapping to record attributes. At least one field is required.
        Example: {'value': 'val', 'value_raw': 'rawval' }

        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=dict, default=None, required=False)
    def geohash_map(self):
        """
        Optional mapping to lat/lon attributes in record for Geohash tag.
        Example: geohash_map = {{'lat': 'latitude', 'lon': 'longitude' }}
        Required: False

        Default: None
        """
        pass

    @Config(ptype=str, default=None, required=False)
    def geohash_wkt_attr(self):
        """
        Optional attribute-name in record that contains a WKT POINT to be used for Geohash tag.
        Example: geohash_wkt_attr = point
        Required: False

        Default: None
        """
        pass

    @Config(ptype=str, required=True)
    def time_attr(self):
        """
        The single required time record attribute to use for InfluxDB time field. NB this attribute
        is now supposed to be a Python datetime object in UTC time. We may add TZ support later.

        Required: True

        Default: N.A.
        """
        pass

    def __init__(self, configdict, section):
        HttpOutput.__init__(self, configdict, section, consumes=FORMAT.record_array)

        # Construct write path
        self.path = '/write?db=%s' % self.database

        # Construct the template line to be used for each data frame
        # e.g. 'joseraw,station=%s,component=%s value=%s %s'
        self.tags_template = None
        if self.tags_map:
            self.tags = self.tags_map.keys()
            self.tags_template = ''
            for tag in self.tags:
                self.tags_template += ',' + tag + '=%s'

        self.geohash_template = None
        if self.geohash_map or self.geohash_wkt_attr:
            self.geohash_template = ',geohash=%s'

        self.fields = self.fields_map.keys()
        self.fields_template = ' '
        for field in self.fields:
            self.fields_template += field + '=%s '

        # will expand to e.g. joseraw,station=19,component=no2raw value=12345 1434055562000000000
        # tags, fields and timestamp will be filled when creating payload
        self.template_data_line = self.measurement + '%s%s%s\n'

    def create_payload(self, packet):
        # Create the POST body (payload) as for example: to host http://data.smartemission.nl:8086/write?db=smartemraw
        # joseraw,station=19,component=no2raw value=12345 1434055562000000000
        # joseraw,station=23,component=temperature value=18 1434055562000000000
        # joseraw,station=19,component=o3raw value=12345 1434055562000000000'

        # Handle both record_array and single record
        records = packet.data
        if type(packet.data) is not list:
            # packet data is single record
            records = [packet.data]

        payload = ''
        nanos = int(1000 * 1000 * 1000) # constant for time conversion

        for record in records:

            # Make Timestamp in Unixtime nanosecs, e.g. 1434055562000000000
            # NB assumed is that time is in UTC!
            # See http://stackoverflow.com/questions/2956886/python-calendar-timegm-vs-time-mktime
            # mktime assumes local timezone!
            # tstamp_nanos = int(time.mktime(record[self.time_attr].timetuple()) * nanos)
            tstamp_nanos = int(calendar.timegm(record[self.time_attr].timetuple()) * nanos)

            # Create optional tags substring
            tags = ''
            if self.tags_template:
                tag_values = []
                for tag in self.tags:
                    tag_values.append(str(record[self.tags_map[tag]]))
                tag_values = tuple(tag_values)
                tags = self.tags_template % tag_values

            # Optional geohash, see https://github.com/vinsci/geohash/
            if self.geohash_template:
                lat = None
                lon = None
                # Option 1: map to record attrs
                if self.geohash_map:
                    lat = record.get(self.geohash_map['lat'])
                    lon = record.get(self.geohash_map['lon'])

                # Option 2: map to WKT-encoded Point in record
                elif self.geohash_wkt_attr:
                    # WKT example: 'SRID=4326;POINT(5.670993 51.472393)'
                    wkt = record.get(self.geohash_wkt_attr)
                    if wkt:
                        # TODO: Poor-man's extraction: should be using regex or geo-lib
                        # NB the order is lon, lat in WKT!
                        lon = float(wkt.split('(')[1].split(' ')[0])
                        lat = float(wkt.split(' ')[1].split(')')[0])

                if lat and lon:
                    geohash = Geohash.encode(lat, lon)
                    geohash_tag = self.geohash_template % geohash
                    tags += geohash_tag

            # Create required fields substring
            field_values = []
            for field in self.fields:
                field_values.append(str(record[self.fields_map[field]]))
            field_values = tuple(field_values)
            fields = self.fields_template % field_values

            # Assemble InfluxDB line protocol string, each measurement on a new line
            payload += self.template_data_line % (tags, fields, tstamp_nanos)

        return payload
