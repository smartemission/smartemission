# -*- coding: utf-8 -*-
#
# Filter to consume a raw record of Smart Emission data (one hour for one device) , refining these, producing records.
#


# Author: Just van den Broecke - 2015

from stetl.util import Util
from stetl.filter import Filter
from stetl.packet import FORMAT

from datetime import datetime
from sensordefs import *

log = Util.get_log("RefineFilter")


class RefineFilter(Filter):
    """
    Filter to consume single raw record with sensor (single hour) timeseries values and produce refined record for each component.
    Refinement entails: calibration (e.g. Ohm to ug/m3) and aggregation (hour-values).
    Input is a single timeseries record for a single hour with all sensorvalues for a single device within that hour.
    """

    def __init__(self, configdict, section):
        Filter.__init__(self, configdict, section, consumes=FORMAT.record, produces=FORMAT.record_array)
        self.current_record = None

    # M = M + (x-M)/n
    # Here M is the (cumulative moving) average, x is the new value in the
    # sequence, n is the count of values.
    def moving_average(self, M, x, n):
        return float(M) + (float(x)-float(M))/float(n)

    def invoke(self, packet):
        if packet.data is None or packet.is_end_of_doc() or packet.is_end_of_stream():
            return packet

        record_in = packet.data

        # list of output records
        records_out = {}

        # ts_list (timeseries list) is an array of dict, each dict containing raw sensor values
        ts_list = record_in['data']['timeseries']
        for ts_dict in ts_list:
            # Go through all the defined outputs we need to calc values for
            for output in OUTPUTS:

                if 'input' not in output or 'converter' not in output:
                    continue

                # get raw input value(s)
                # i.e. in some cases multiple inputs are required (e.g. audio bands)
                input_name = output['input']
                value_raw = get_raw_value(input_name, ts_dict)
                if value_raw is None:
                    # No use to proceed without raw input value(s)
                    continue

                # First all common attrs (device_id, time, staleness etc)
                output_name = output['name']
                value_avg = None
                value_raw_avg = None
                if output_name not in records_out:
                    # Start new record with common data
                    record = dict()
                    record['device_id'] = record_in['device_id']
                    record['day'] = record_in['day']
                    record['hour'] = record_in['hour']
                    record['name'] = output_name
                    record['label'] = output['label']
                    record['unit'] = output['unit']
                    record['sample_count'] = 0
                else:
                    # Record already exists: will add to average later
                    record = records_out[output_name]
                    if 'value' in record:
                        value_avg = record['value']
                    if 'value_raw' in record:
                        value_raw_avg = record['value_raw']

                # Calculate values, also keep raw value, min and max
                record['sample_count'] += 1
                if value_raw_avg is not None:
                    # M = M + (x-M)/n
                    # Here M is the (cumulative moving) average, x is the new value in the
                    # sequence, n is the count of values.
                    record['value_raw'] = self.moving_average(value_raw_avg, value_raw, record['sample_count'])
                else:
                    # First value for avg
                    record['value_raw'] = value_raw

                value = output['converter'](value_raw, ts_dict, output_name)
                if value is not None:
                    if value_avg is not None:
                        # Recalc avg
                        record['value'] = self.moving_average(value_avg, value, record['sample_count'])

                        # Set min/max
                        if value < record['value_min']:
                            record['value_min'] = value
                        if value > record['value_max']:
                            record['value_max'] = value
                    else:
                        # First value for avg
                        record['value'] = value
                        record['value_min'] = value
                        record['value_max'] = value

                if record['value'] is not None:
                    records_out[output_name] = record

                # if output_name == 'v_audiolevel' and 'v_audioavg' in ts_list:
                #     # average dB value as raw value
                #     record['value_raw'] = ts_dict['v_audioavg']

        packet.data = records_out.values()
        for rec in packet.data:
            rec['value'] = int(round(rec['value']))
            rec['value_raw'] = int(round(rec['value_raw']))
        return packet
