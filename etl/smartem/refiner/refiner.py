# -*- coding: utf-8 -*-
#
# Consume a raw record of Smart Emission data (one hour for one device), refining these, producing records.
#


# Author: Just van den Broecke - 2015-2018
import sys
import traceback
import math
import pytz
from datetime import datetime, timedelta

from smartem.devices.devicereg import DeviceReg
import logging

log = logging.getLogger('Refiner')


class Refiner:
    # Refiner instance is Singleton: one per process.
    refiners = {}
    
    def __init__(self, device):
        self.device = device
        self.config_dict = None

    @staticmethod
    def get_refiner(device_type):
        """
        Get Refiner for device type, Singleton factory function.

        :param device_type:  e.g. "jose" or "ase"
        :return Refiner instance: single instance for device type
        """
        if device_type not in Refiner.refiners:
            device = DeviceReg.get_device(device_type)
            if not device:
                log.warn('No Device available for device_type=%s (no Device class found)' % device_type)
                return None

            Refiner.refiners[device_type] = Refiner(device)

        return Refiner.refiners[device_type]

    def init(self, config_dict):
        """
        Initialize with dict of config parameters.
        :param config_dict:
        :return:
        """

        self.config_dict = config_dict
        self.device.init(self.config_dict)

    def exit(self):
        self.device.exit()

    # M = M + (x-M)/n
    # Here M is the (cumulative moving) average, x is the new value in the
    # sequence, n is the count of values. Using floats as not to loose precision.
    def moving_average(self, moving_avg, x, n, unit):
        if 'dB' in unit:
            # convert Decibel to Bel and then get "real" value (power 10)
            # print moving_avg, x, n
            x = math.pow(10, x / 10)
            moving_avg = math.pow(10, moving_avg / 10)
            moving_avg = self.moving_average(moving_avg, x, n, 'int')
            # Take average of "real" values and convert back to Bel via log10 and Decibel via *10
            return math.log10(moving_avg) * 10.0

        # Standard moving avg.
        return float(moving_avg) + (float(x) - float(moving_avg)) / float(n)

    def refine(self, record_in, sensor_names):
        # Start dict of output records, key is sensor name, value is a record
        records_out = dict()

        gid_raw = -1
        day = -1
        hour = -1
        if 'gid' in record_in:
            gid_raw = record_in['gid']
        if 'day' in record_in:
            day = record_in['day']
        if 'hour' in record_in:
            hour = record_in['hour']

        device_id = record_in['device_id']
        device_meta = self.device.get_meta_id(record_in['device_version'])

        # ts_list (timeseries list) is an array of dict, each dict containing raw sensor values
        ts_list = record_in['data']['timeseries']
        unique_id = 'device %d' % device_id
        if 'unique_id' in record_in:
            unique_id = record_in['unique_id']

        log.info('processing unique_id=%s gid_raw=%d ts_count=%d' % (unique_id, gid_raw, len(ts_list)))

        validate_errs = 0
        sensor_defs = self.device.get_sensor_defs()

        # Go through each record in timeseries list for single device
        for sensor_vals in ts_list:
            # Go through all the configured sensor outputs we need to calc values for
            for sensor_name in sensor_names:
                record = None
                try:
                    sensor_def = self.device.get_sensor_def(sensor_name)
                    if not sensor_def:
                        # log.warn('Sensor name %s not defined for device_meta=%s dev_id=%s' %
                        #          (sensor_name, device_meta, str(device_id)))
                        continue

                    if 'input' not in sensor_def or 'converter' not in sensor_def:
                        log.warn('No input or converter defined for %s device_meta=%s dev_id=%s' %
                                                         (sensor_name, device_meta, str(device_id)))
                        continue

                    # In some cases the sensor_vals are unrelated to the sensor_name (mainly ASE)
                    if not self.device.can_resolve(sensor_name, sensor_vals):
                        continue

                    # get raw input value(s)
                    # i.e. in some cases multiple inputs are required (e.g. audio bands)
                    input_name = sensor_def['input']
                    input_valid, reason = self.device.check_value(input_name, sensor_vals)
                    if not input_valid:
                        log.warn('id=%d-%d-%d-%s meta=%s gid_raw=%d: invalid input for %s: detail=%s' % (
                           device_id, day, hour, sensor_name, device_meta, gid_raw, str(input_name), reason))
                        validate_errs += 1
                        continue

                    value_raw, input_name_0 = self.device.get_raw_value(input_name, sensor_vals)
                    if value_raw is None:
                        # No use to proceed without raw input value(s)
                        validate_errs += 1
                        continue

                    # First all common attrs (device_id, time etc)
                    value_avg = None
                    value_raw_avg = None
                    if sensor_name not in records_out:
                        # Start new record with common data
                        # Subsequent data will be averaged.
                        record = dict()

                        # gid_raw refers to harvested record, optional
                        if gid_raw > 0:
                            record['gid_raw'] = gid_raw

                        record['device_id'] = device_id
                        record['device_meta'] = device_meta
                        record['sensor_meta'] = self.device.get_sensor_meta_id(sensor_name, sensor_vals)

                        # Optional fields dependent on input record
                        if 'value_stale' in record_in:
                            record['value_stale'] = record_in['value_stale']

                        if 'device_name' in record_in:
                            record['device_name'] = record_in['device_name']

                        if 'unique_id' not in record_in:
                            record['unique_id'] = '%d-%s' % (device_id, sensor_name)

                        if day > 0:
                            record['day'] = day
                            record['hour'] = hour

                            # GMT does not know about 24 so we move to 00:00 the next day
                            day_hour = str(day) + str(hour)
                            if hour == 24:
                                # Need to move to 00:00 next day if hour is 24
                                # Just incrementing the day +1 is not enough: we may need to skip to next month
                                # http://stackoverflow.com/questions/3240458/how-to-increment-the-day-in-datetime-python
                                next_day = datetime.strptime('%sGMT' % str(day), '%Y%m%dGMT').replace(tzinfo=pytz.utc)
                                next_day += timedelta(days=1)
                                day_hour = next_day.strftime('%Y%m%d') + '0'

                            record['time'] = datetime.strptime('%sGMT' % day_hour, '%Y%m%d%HGMT').replace(tzinfo=pytz.utc)
                        else:
                            record['time'] = record_in['time']

                        record['name'] = sensor_name
                        record['label'] = sensor_def['label']
                        record['unit'] = sensor_def['unit']
                        record['sample_count'] = 0

                        # Point location TODO: average, but for now assume static
                        lon, lat = self.device.get_lon_lat(sensor_vals)
                        if lon and lat:
                            # Both lat and lon are valid!
                            record['point'] = 'SRID=4326;POINT(%f %f)' % (lon, lat)

                        # No 'point' proceeding without a location
                        if 'point' not in record:
                            log.warn('id=%d-%d-%d-%s meta=%s gid_raw=%d: no GPS location' % (
                               device_id, day, hour, sensor_name, device_meta, gid_raw))
                            validate_errs += 1
                            continue

                        # GPS height. TODO use air pressure
                        record['altitude'] = 0
                        if 's_altimeter' in sensor_vals:
                            altitude = sensor_defs['altitude']['converter'](sensor_vals['s_altimeter'])
                            valid, reason = self.device.check_value('altitude', sensor_vals, value=altitude)
                            if not valid:
                                altitude = 0

                            # altitude valid!
                            record['altitude'] = altitude

                    else:
                        # Record for sensor_name already exists: will add to average later
                        record = records_out[sensor_name]
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
                        record['value_raw'] = self.moving_average(value_raw_avg, value_raw, record['sample_count'],
                                                                  sensor_defs[input_name_0]['unit'])
                    else:
                        # First value for avg
                        record['value_raw'] = value_raw

                    # Do the conversion/calibration in 3 steps
                    # 1) check inputs (available and valid)
                    # 2) convert
                    # 3) check output (available and valid)

                    # 1) check inputs
                    sensor_vals['device_id'] = device_id
                    value = sensor_def['converter'](value_raw, sensor_vals, sensor_def, self.device)
                    output_valid, reason = self.device.check_value(sensor_name, sensor_vals, value=value)
                    if not output_valid:
                        log.warn('id=%d-%d-%d-%s gid_raw=%d: invalid output for %s: detail=%s' % (
                            device_id, day, hour, sensor_name, gid_raw, sensor_name, reason))
                        validate_errs += 1
                        continue

                    # Finally calculate calibrated value and recalc  average
                    if value_avg is not None:
                        # Recalc avg
                        record['value'] = self.moving_average(value_avg, value, record['sample_count'], sensor_def['unit'])

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

                except Exception as e:
                    log.error('Exception refining %s gid_raw=%d dev=%d day-hour=%d-%d, err=%s' % (
                        sensor_name, gid_raw, device_id, day, hour, str(e)))
                    traceback.print_exc(file=sys.stdout)
                else:
                    # No error and output value: assign record to result list
                    if record and 'value' in record:
                        records_out[sensor_name] = record

                        # if output_name == 'v_audiolevel' and 'v_audioavg' in ts_list:
                        #     # average dB value as raw value
                        #     record['value_raw'] = sensor_vals['v_audioavg']

        # make records into a list() and round all (raw) values
        records_out = records_out.values()

        # Values are float, all outputs should be ints, so round
        for rec in records_out:
            rec['value'] = int(round(rec['value']))
            rec['value_raw'] = int(round(rec['value_raw']))
            if 'last' in record_in:
                rec.pop('sample_count')
                rec.pop('value_min')
                rec.pop('value_max')

        log.info('Result unique_id=%s gid_raw=%d record_count=%d val_errs=%d' % (unique_id, gid_raw, len(records_out), validate_errs))
        return records_out
