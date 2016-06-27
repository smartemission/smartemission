# -*- coding: utf-8 -*-
#
# Filter to consume a raw record of Smart Emission data (one hour for one device) , refining these, producing records.
#


# Author: Just van den Broecke - 2015

from stetl.util import Util
from stetl.filter import Filter
from stetl.packet import FORMAT

from datetime import datetime
import json
from sensorconverters import convert

log = Util.get_log("RefineFilter")


class RefineFilter(Filter):
    """
    Filter to consume single raw record with sensor (hour) timeseries values and produce refined recod.
    """

    def __init__(self, configdict, section):
        Filter.__init__(self, configdict, section, consumes=FORMAT.record, produces=FORMAT.record_array)
        self.current_record = None

    def invoke(self, packet):
        if packet.data is None or packet.is_end_of_doc() or packet.is_end_of_stream():
            return packet

        record_in = packet.data

        # Base data for all records
        record_out = {}
        record_out['device_id'] = record_in['device_id']
        record_out['device_name'] = 'station %d' % record_out['device_id']

        ts_list = record_in['data']['timeseries']
        for ts in ts_list:
            print str(ts)

        packet.data = record_out
        return packet
