# -*- coding: utf-8 -*-
#
# Filter to consume a raw record of Smart Emission data (one hour for one
# device), and subtract these, producing records.
#


# Author: Pieter Marsman - 2016
import sys
import traceback
from stetl.component import Config
from stetl.filter import Filter
from stetl.packet import FORMAT
from stetl.util import Util

from dateutil import parser

from sensordefs import *

log = Util.get_log("SubtractFilter")


class SubtractFilter(Filter):
    """
    Filter to consume single raw record with sensor (single hour) timeseries values and subtract these for each component.
    Input is a single timeseries record for a single hour with all sensorvalues for a single device within that hour.
    """

    @Config(ptype=list, default=[], required=True)
    def sensor_names(self):
        """
        The output sensor names to subtract.

        Required: True

        Default: []
        """
        pass

    def __init__(self, configdict, section):
        Filter.__init__(self, configdict, section, consumes=FORMAT.record,
                        produces=FORMAT.record_array)
        self.current_record = None

    def invoke(self, packet):
        if packet.data is None or packet.is_end_of_doc() or packet.is_end_of_stream():
            return packet

        # The TS input record: single device with json-field with list of dict for values
        record_in = packet.data

        # Start list of output records
        records_out = []

        # ts_list (timeseries list) is an array of dict, each dict containing raw sensor values
        device_id = record_in['device_id']
        unique_id = record_in['unique_id']
        gid_raw = record_in['gid']
        validate_errs = 0

        ts_list = record_in['data']['timeseries']
        log.info('processing unique_id=%s gid_raw=%d ts_count=%d' % (
            unique_id, gid_raw, len(ts_list)))

        for sensor_vals in ts_list:
            # log.debug(str(sensor_vals))

            if 'time' not in sensor_vals:
                log.warn('Sensor values without time are of no use')
                continue

            # Go through all the configured sensor outputs we need to calc values for
            for sensor_name in self.sensor_names:

                try:
                    # sensor name should be in sensor defs
                    record = dict()
                    record['device_id'] = device_id
                    record['time'] = parser.parse(sensor_vals['time'])
                    record['name'] = sensor_name

                    if sensor_name not in SENSOR_DEFS:
                        log.warn(
                            'Sensor name %s not defined in SENSOR_DEFS' % sensor_name)
                        continue

                    # sensor def should have an input and converter elements
                    sensor_def = SENSOR_DEFS[sensor_name]
                    if 'input' not in sensor_def or 'converter' not in sensor_def:
                        log.warn(
                            'No input or converter defined for %s in SENSOR_DEFS' % sensor_name)
                        continue

                    # get raw input value(s)
                    # i.e. in some cases multiple inputs are required (e.g. audio bands)
                    input_name = sensor_def['input']
                    input_valid, reason = check_value(input_name, sensor_vals)
                    if not input_valid:
                        # log.warn('id=%d-%d-%d-%s gid_raw=%d: invalid input for %s: detail=%s' % (
                        # device_id, day, hour, sensor_name, gid_raw, str(input_name), reason))
                        validate_errs += 1
                        continue

                    # value should be available
                    value_raw, input_name_0 = get_raw_value(input_name,
                                                            sensor_vals)
                    if value_raw is None:
                        # No use to proceed without raw input value(s)
                        log.warn('Value raw is None for %s' % sensor_name)
                        validate_errs += 1
                        continue

                    record['value'] = value_raw

                except Exception, e:
                    log.error('Exception refining gid_raw=%d dev=%d, err=%s' % (
                        gid_raw, device_id, str(e)))
                    traceback.print_exc(file=sys.stdout)
                else:
                    # Only save results when measuring something
                    records_out.append(record)

        packet.data = records_out
        log.info(
            'Result unique_id=%s gid_raw=%d record_count=%d val_errs=%d' % (
                unique_id, gid_raw, len(records_out), validate_errs))

        return packet
