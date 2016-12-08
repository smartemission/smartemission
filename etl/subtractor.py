# -*- coding: utf-8 -*-
#
# Filter to consume a raw record of Smart Emission data (one hour for one
# device), and subtract these, producing records.
#


# Author: Just van den Broecke - 2015
import sys, traceback

from stetl.filter import Filter
from stetl.util import Util
from stetl.packet import FORMAT
from stetl.component import Config

from datetime import datetime, timedelta
import pytz
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
        Filter.__init__(self, configdict, section, consumes=FORMAT.record, produces=FORMAT.record_array)
        self.current_record = None

    # M = M + (x-M)/n
    # Here M is the (cumulative moving) average, x is the new value in the
    # sequence, n is the count of values. Using floats as not to loose precision.
    def moving_average(self, M, x, n, unit):
        if 'dB' in unit:
            # convert Decibel to Bel and then get "real" value (power 10)
            # print M, x, n
            x = math.pow(10, x / 10)
            M = math.pow(10, M / 10)
            M = self.moving_average(M, x, n, 'int')
            # Take average of "real" values and convert back to Bel via log10 and Decibel via *10
            return math.log10(M) * 10.0

        return float(M) + (float(x) - float(M)) / float(n)

    def invoke(self, packet):
        if packet.data is None or packet.is_end_of_doc() or packet.is_end_of_stream():
            return packet

        # The TS input record: single device with json-field with list of dict for values
        record_in = packet.data

        # Start list of output records
        records_out = []

        # ts_list (timeseries list) is an array of dict, each dict containing raw sensor values
        ts_list = record_in['data']['timeseries']
        gid_raw = record_in['gid']
        unique_id = record_in['unique_id']
        log.info('processing unique_id=%s gid_raw=%d ts_count=%d' % (unique_id, gid_raw, len(ts_list)))
        device_id = record_in['device_id']
        day = record_in['day']
        hour = record_in['hour']
        validate_errs = 0
        for sensor_vals in ts_list:
            # log.debug(str(sensor_vals))
            # Go through all the configured sensor outputs we need to calc values for
            for sensor_name in self.sensor_names:
                record = None
                try:
                    # sensor name should be in sensor defs
                    if sensor_name not in SENSOR_DEFS:
                        log.warn('Sensor name %s not defined in SENSOR_DEFS' % sensor_name)
                        continue

                    # sensor def should have an input and converter elements
                    sensor_def = SENSOR_DEFS[sensor_name]
                    if 'input' not in sensor_def or 'converter' not in sensor_def:
                        log.warn('No input or converter defined for %s in SENSOR_DEFS' % sensor_name)
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
                    value_raw, input_name_0 = get_raw_value(input_name, sensor_vals)
                    if value_raw is None:
                        # No use to proceed without raw input value(s)
                        log.warn('Value raw is None for %s' % sensor_name)
                        validate_errs += 1
                        continue

                    # # First all common attrs (device_id, time etc)
                    # value_avg = None
                    # value_raw_avg = None


                    # if sensor_name not in records_out:
                    # Start new record with common data
                    record = dict()
                    # gid_raw refers to harvested record
                    # record['gid_raw'] = gid_raw
                    record['device_id'] = device_id
                    # record['day'] = day
                    # record['hour'] = hour

                    # # GMT does not know about 24 so we move to 00:00 the next day
                    # day_hour = str(day) + str(hour)
                    # if hour == 24:
                    #     # Need to move to 00:00 next day if hour is 24
                    #     # Just incrementing the day +1 is not enough: we may need to skip to next month
                    #     # http://stackoverflow.com/questions/3240458/how-to-increment-the-day-in-datetime-python
                    #     next_day = datetime.strptime('%sGMT' % str(day), '%Y%m%dGMT').replace(tzinfo=pytz.utc)
                    #     next_day += timedelta(days=1)
                    #     day_hour = next_day.strftime('%Y%m%d') + '0'
                    #
                    # record['time'] = datetime.strptime('%sGMT' % day_hour, '%Y%m%d%HGMT').replace(tzinfo=pytz.utc)
                    record['time'] = sensor_vals['time']
                    record['name'] = sensor_name
                    # record['label'] = sensor_def['label']
                    # record['unit'] = sensor_def['unit']
                    # record['sample_count'] = 0

                    # # Point location TODO: average, but for now assume static
                    # if 's_longitude' in sensor_vals and 's_latitude' in sensor_vals:
                    #     lon = SENSOR_DEFS['longitude']['converter'](sensor_vals['s_longitude'])
                    #     lat = SENSOR_DEFS['latitude']['converter'](sensor_vals['s_latitude'])
                    #
                    #     valid, reason = check_value('latitude', sensor_vals, value=lat)
                    #     if not valid:
                    #         log.warn('Latitude is not valid')
                    #         validate_errs += 1
                    #         continue
                    #
                    #     valid, reason = check_value('longitude', sensor_vals, value=lon)
                    #     if not valid:
                    #         log.warn('Longitude is not valid')
                    #         validate_errs += 1
                    #         continue
                    #
                    #     # Both lat and lon are valid!
                    #     record['point'] = 'SRID=4326;POINT(%f %f)' % (lon, lat)
                    #
                    # # No 'point' proceeding without a location
                    # if 'point' not in record:
                    #     log.warn('No point in proceding without location')
                    #     validate_errs += 1
                    #     continue

                    # # GPS height. TODO use air pressure
                    # record['altitude'] = 0
                    # if 's_altimeter' in sensor_vals:
                    #     altitude = SENSOR_DEFS['altitude']['converter'](sensor_vals['s_altimeter'])
                    #     valid, reason = check_value('altitude', sensor_vals, value=altitude)
                    #     if not valid:
                    #         altitude = 0
                    #
                    #     # altitude valid!
                    #     record['altitude'] = altitude

                    # else:
                    #     # Record for sensor_name already exists: will add to average later
                    #     record = records_out[sensor_name]
                    #     if 'value' in record:
                    #         value_avg = record['value']
                    #     if 'value_raw' in record:
                    #         value_raw_avg = record['value_raw']

                    # # Calculate values, also keep raw value, min and max
                    # record['sample_count'] += 1
                    # if value_raw_avg is not None:
                    #     # M = M + (x-M)/n
                    #     # Here M is the (cumulative moving) average, x is the new value in the
                    #     # sequence, n is the count of values.
                    #     record['value_raw'] = self.moving_average(value_raw_avg, value_raw, record['sample_count'],
                    #                                               SENSOR_DEFS[input_name_0]['unit'])
                    # else:
                    #     # First value for avg
                    record['value_raw'] = value_raw


                    # Do the conversion/calibration in 3 steps
                    # 1) check inputs (available and valid)
                    # 2) convert
                    # 3) check output (available and valid)

                    # 1) check inputs

                    # At this point the data for calibration should be saved


                    # value = sensor_def['converter'](value_raw, sensor_vals, sensor_def)
                    # output_valid, reason = check_value(sensor_name, sensor_vals, value=value)
                    # if not output_valid:
                    #     log.warn('id=%d-%d-%d-%s gid_raw=%d: invalid output for %s: detail=%s' % (
                    #         device_id, day, hour, sensor_name, gid_raw, sensor_name, reason))
                    #     validate_errs += 1
                    #     continue

                    # Finally calculate calibrated value and recalc  average
                    # if value_avg is not None:
                    #     # Recalc avg
                    #     record['value'] = self.moving_average(value_avg, value, record['sample_count'], sensor_def['unit'])
                    #
                    #     # Set min/max
                    #     if value < record['value_min']:
                    #         record['value_min'] = value
                    #     if value > record['value_max']:
                    #         record['value_max'] = value
                    # else:
                    #     # First value for avg
                    #     record['value'] = value
                    #     record['value_min'] = value
                    #     record['value_max'] = value

                except Exception, e:
                    log.error('Exception refining %s gid_raw=%d dev=%d day-hour=%d-%d, err=%s' % (
                        sensor_name, gid_raw, device_id, day, hour, str(e)))
                    traceback.print_exc(file=sys.stdout)
                else:
                    # No error and output value: assign record to result list
                    if record and 'value_raw' in record:
                        records_out.append(record)

                        # if output_name == 'v_audiolevel' and 'v_audioavg' in ts_list:
                        #     # average dB value as raw value
                        #     record['value_raw'] = sensor_vals['v_audioavg']

        # make records into a list() and round all (raw) values
        # records_out = records_out.values()

        # Values are float, all outputs should be ints, so round
        for rec in records_out:
            # rec['value'] = int(round(rec['value']))
            rec['value_raw'] = int(round(rec['value_raw']))

        packet.data = records_out
        log.info('Result unique_id=%s gid_raw=%d record_count=%d val_errs=%d' % (unique_id, gid_raw, len(records_out), validate_errs))
        return packet
