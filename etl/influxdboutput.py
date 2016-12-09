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
    """

    @Config(ptype=str, default='joseraw', required=False)
    def measurement(self):
        """
        .

        Required: False

        Default: joseraw
        """
        pass

    @Config(ptype=list, default=['station', 'component'], required=False)
    def tag_keys(self):
        """
        The tag keys.

        Required: False

        Default: ['value']
        """
        pass

    @Config(ptype=list, default=['value'], required=False)
    def field_keys(self):
        """
        The value fields.

        Required: False

        Default: ['value']
        """
        pass

    def __init__(self, configdict, section):
        HttpOutput.__init__(self, configdict, section, consumes=FORMAT.record_array)

        # Construct the template line for each data frame
        self.template_data_line = self.measurement + ',station=%d,component=%s value=%d %s'

    def create_payload(self, packet):
        # Create the POST payload as for example: to host http://data.smartemission.nl:8086/write?db=smartemraw
        # joseraw,station=19,component=no2raw value=12345 1434055562000000000
        # joseraw,station=23,component=temperature value=18 1434055562000000000
        # joseraw,station=19,component=o3raw value=12345 1434055562000000000'

        record = packet.data

        # Make Timestamp in Unixtime nanosecs, e.g. 1434055562000000000
        t = record['time']
        tstamp = int(time.mktime(t.timetuple())) * 1000 * 1000

        # Create InfluxDB line protocol string
        payload = self.template_data_line % (record['device_id'], record['name'], record['value'], tstamp)

        return payload
