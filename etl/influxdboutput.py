#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output classes for ETL: write record_array to InfluxDB database server via HTTP.
#
# Author: Just van den Broecke
#
import time

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
        The "measurement" is a table-like entity in an InfluxDB database

        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=dict, required=True)
    def tags_map(self):
        """
        The tag keys, sort of free-to-choose columns with their mappings to attributes in incoming records.
        Example: {'station': 'device_id', 'component': 'name' }
        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=dict, required=True)
    def fields_map(self):
        """
        The actual value fields with their mapping to record attributes.

        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=str, required=True)
    def time_attr(self):
        """
        The time record attribute to use for InfluxDB time field.

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
        self.tags = self.tags_map.keys()
        self.fields = self.fields_map.keys()
        self.tags_template = ''
        for tag in self.tags:
            self.tags_template += ',' + tag + '=%s'

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
            # delete: DELETE FROM joseraw WHERE time > '1970-01-01'
            tstamp_nanos = int(time.mktime(record[self.time_attr].timetuple()) * nanos)

            # Create tags substring
            tag_values = []
            for tag in self.tags:
                tag_values.append(str(record[self.tags_map[tag]]))
            tag_values = tuple(tag_values)
            tags = self.tags_template % tag_values

            # Create fields substring
            field_values = []
            for field in self.fields:
                field_values.append(str(record[self.fields_map[field]]))
            field_values = tuple(field_values)
            fields = self.fields_template % field_values

            # Assemble InfluxDB line protocol string, each measurement on a new line
            payload += self.template_data_line % (tags, fields, tstamp_nanos)

        return payload
