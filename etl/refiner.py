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

log = Util.get_log("RefineFilter")


class RefineFilter(Filter):
    """
    Filter to consume raw records with sensor timeseries values.
    """

    def __init__(self, configdict, section):
        Filter.__init__(self, configdict, section, consumes=FORMAT.record, produces=FORMAT.record_array)
        self.current_record = None
        
    def parse_json_str(self, raw_str):
        # Parse JSON from data string
        json_obj = None
        try:
            json_obj = json.loads(raw_str)
        except Exception, e:
            log.error('Cannot parse JSON from %s, err= %s' % (raw_str, str(e)))
            raise e

        return json_obj

    def invoke(self, packet):
        if packet.data is None or packet.is_end_of_doc() or packet.is_end_of_stream():
            return packet

        ts_list = packet.data['data']['timeseries']
        for ts in ts_list:
            print str(ts)
        return packet
