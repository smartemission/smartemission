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
from sensordefs import OUTPUTS
from sensorconverters import convert

log = Util.get_log("RefineFilter")


class RefineFilter(Filter):
    """
    Filter to consume single raw record with sensor (hour) timeseries values and produce refined record.
    Refinement entails: calibration (e.g. Ohm to ug/m3) and aggregation (hour-values).
    Input is a single timeseries record for a single hour with all sensorvalues for a single device within that hour.
    """

    def __init__(self, configdict, section):
        Filter.__init__(self, configdict, section, consumes=FORMAT.record, produces=FORMAT.record_array)
        self.current_record = None

    def invoke(self, packet):
        if packet.data is None or packet.is_end_of_doc() or packet.is_end_of_stream():
            return packet

        record_in = packet.data

        # list of output records
        records_out = {}

        # ts_list is an array of dict, each dict containing sensro values
        ts_list = record_in['data']['timeseries']
        for ts_dict in ts_list:
            for output in OUTPUTS:
                name = output['name']
                value_avg = None
                value_raw_avg = None

                # First all common attrs (device_id, time, staleness etc)
                if name not in records_out:
                    # Base data for all records
                    record = {}
                    record['device_id'] = record_in['device_id']
                    record['day'] = record_in['day']
                    record['hour'] = record_in['hour']
                    record['id'] = output['id']
                    record['unique_id'] = '%d-%d' % (record['device_id'], record['id'])
                    record['name'] = name
                    record['label'] = output['label']
                    record['unit'] = output['unit']
                    record['sample_count'] = 0
                    records_out[name] = record
                else:
                    record = records_out[name]
                    if 'value' in record:
                        value_avg = record['value']
                    if 'value_raw' in record:
                        value_raw_avg = record['value_raw']

                if name in ts_dict:
                    record['sample_count'] += 1
                    sample_count = record['sample_count']
                    cur_value_raw = ts_dict[name]
                    if cur_value_raw is not None:
                        if value_raw_avg is not None:
                            record['value_raw'] = (value_raw_avg + cur_value_raw)/sample_count
                        else:
                            # First value for avg
                            record['value_raw'] = cur_value_raw

                    cur_value = convert(ts_dict, name)
                    if cur_value is not None:
                        if value_avg is not None:
                            # Recalc hour avg
                            record['value'] = (value_avg + cur_value)/sample_count
                        else:
                            # First value for avg
                            record['value'] = cur_value

                    if record['value'] is None:
                        continue

                    if name == 's_o3' and 's_o3resistance' in ts_dict:
                        # average dB value as raw value
                        record['value_raw'] = ts_dict['s_o3resistance']

                    if name == 'v_audiolevel' and 'v_audioavg' in ts_list:
                        # average dB value as raw value
                        record['value_raw'] = ts_dict['v_audioavg']

        packet.data = records_out.values()
        return packet
