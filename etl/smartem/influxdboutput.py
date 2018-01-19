#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output classes for ETL: write record_array to InfluxDB database server via HTTP.
#
# Author: Just van den Broecke
#

import calendar
import Geohash

from stetl.outputs.httpoutput import HttpOutput
from stetl.util import Util
from stetl.packet import FORMAT
from stetl.component import Config

log = Util.get_log('influxdboutput')

# constant for time conversion
NANOS = int(1000 * 1000 * 1000)


class InfluxDbOutput(HttpOutput):
    """
    Output via InfluxDB protocol over plain HTTP.
    Optional support for geohash fields and/or tags (see https://en.wikipedia.org/wiki/Geohash).
    Indicated in config via geohash_wkt_attr or geohash_map (which fields to map as lat/lon from record).
    TODO: use the official Python InfluxDB Client (see InfluxDbInput)

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
        fields_map = {{'value': 'value'}}
        geohash_tag= True
        geohash_tag_name = 'geohashtag'
        geohash_tag_precision = 7 # about 70-80 meters
        geohash_field = True
        geohash_field_name = 'geohash'
        geohash_field_precision = 12
        geohash_wkt_attr = point  or geohash_map = {{'lat': 'lat', 'lon': 'lon' }}
        time_attr = time
        user = theuser
        password = thepass

    """

    @Config(ptype=str, required=True)
    def database(self):
        """
        The "database" is a db-like entity in an InfluxDB server instance.

        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=str, required=True)
    def measurement(self):
        """
        The required "measurement" is a table-like entity in an InfluxDB database.

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

    @Config(ptype=bool, default=False, required=False)
    def geohash_tag(self):
        """
        Add a geohash encoded lat/lon tag?

        Default: False

        Required: False
        """

    @Config(ptype=str, default='geohash_tag', required=False)
    def geohash_tag_name(self):
        """
        Optional name for the geohash tag.

        Default: 'geohash_tag'

        Required: False
        """

    @Config(ptype=int, default=7, required=False)
    def geohash_tag_precision(self):
        """
        Precision for the geohash when used as tag. Number of characters to use in the
        geohash. See https://en.wikipedia.org/wiki/Geohash.

        Default: 7 (course: about 70-80)

        Required: False
        """

    @Config(ptype=bool, default=False, required=False)
    def geohash_field(self):
        """
        Add a geohash encoded lat/lon field?

        Default: False

        Required: False
        """

    @Config(ptype=str, default='geohash', required=False)
    def geohash_field_name(self):
        """
        Optional name for the geohash field.

        Default: 'geohash'

        Required: False
        """

    @Config(ptype=int, default=12, required=False)
    def geohash_field_precision(self):
        """
        Precision for the geohash when used as field. Number of characters to use in the
        geohash.  See https://en.wikipedia.org/wiki/Geohash.

        Default: 12

        Required: False
        """


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
        # We split into separate sub-templates for tags, fields, optional geohashes

        # Optional Tags template
        self.tags_template = None
        if self.tags_map:
            self.tags = self.tags_map.keys()
            self.tags_template = ''
            for tag in self.tags:
                if self.tags_template:
                    # Additional tags
                    self.tags_template += ',' + tag + '=%s'
                else:
                    # First or one tag
                    self.tags_template = tag + '=%s'

        # Required Fields template (need at least one field)
        self.fields_template = None
        self.fields = self.fields_map.keys()
        for field in self.fields:
            if self.fields_template:
                # Additional fields
                self.fields_template += ',' + field + '=%s'
            else:
                # First or one field
                self.fields_template = field + '=%s'

        # Optional extra geohash as tag template
        if self.geohash_tag:
            self.geohash_tag_template = ',' + self.geohash_tag_name + '=%s'

        # Optional extra geohash as field template
        if self.geohash_field:
            self.geohash_field_template = ',' + self.geohash_field_name + '="%s"'

        # will expand to <measurement>,<tags> <fields>
        # e.g. joseraw,station=19,component=no2raw value=12345,geohash_tag=uvx53kryp 1434055562000000000
        # tags, fields and timestamp will be substituted when creating payload
        self.template_data_line = self.measurement + ',%s %s %d\n'

    def create_payload(self, packet):
        """
         Create the POST body (payload) as string using InfluxDB Line Protocol,
         for example: to host http://data.smartemission.nl:8086/write?db=smartemraw

           joseraw,station=19,component=no2raw value=12345 1434055562000000000
           joseraw,station=23,component=temperature value=18 1434055562000000000
           joseraw,station=19,component=o3raw value=12345 1434055562000000000

        """

        # Handle both record_array and single record
        records = packet.data
        if type(packet.data) is not list:
            # packet data is single record
            records = [packet.data]

        log.info("Creating payload from %d records" % len(records))

        payload = ''

        for record in records:

            # Make Timestamp in Unixtime nanosecs, e.g. 1434055562000000000
            # NB assumed is that input time attr is in UTC!
            # See http://stackoverflow.com/questions/2956886/python-calendar-timegm-vs-time-mktime
            # mktime assumes local timezone!
            # tstamp_nanos = int(time.mktime(record[self.time_attr].timetuple()) * nanos)
            tstamp_nanos = int(calendar.timegm(record[self.time_attr].timetuple()) * NANOS)

            # Create optional tags substring using template
            tags = ''
            if self.tags_template:
                tag_values = []
                for tag in self.tags:
                    tag_values.append(str(record[self.tags_map[tag]]))
                tag_values = tuple(tag_values)
                tags = self.tags_template % tag_values

            # Create required field(s) substring using template
            field_values = []
            for field in self.fields:
                field_values.append(str(record[self.fields_map[field]]))
            field_values = tuple(field_values)
            fields = self.fields_template % field_values

            # Optional geohash as field and/or tag,
            # see https://github.com/vinsci/geohash/
            if self.geohash_tag or self.geohash_field:
                lat = None
                lon = None

                # Determine where to get lat/lon from
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
                    if self.geohash_tag:
                        geohash_tag_val = Geohash.encode(lat, lon, self.geohash_tag_precision)
                        geohash_tag = self.geohash_tag_template % geohash_tag_val
                        tags += geohash_tag
                        
                    if self.geohash_field:
                        geohash_field_val = Geohash.encode(lat, lon, self.geohash_field_precision)
                        geohash_field = self.geohash_field_template % geohash_field_val
                        fields += geohash_field

            # Assemble InfluxDB line protocol string, each measurement on a new line
            payload += self.template_data_line % (tags, fields, tstamp_nanos)

        log.info("Created payload of %d characters" % len(payload))

        return payload
