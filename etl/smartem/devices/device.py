# -*- coding: utf-8 -*-
#
# Abstraction of a "station" or "sensor device", base class for specific
# device types like Josene and AirSensEUR.
#
# Author: Just van den Broecke - 2015-2018

import logging

log = logging.getLogger('Device')


class Device:
    """
    Abstraction of a "station" or "sensor device", base class for specific
    device types like Josene and AirSensEUR.
    """

    def __init__(self, type):
        self.device_type = type

    def init(self, config):
        pass

    def exit(self):
        pass

    def can_resolve(self, sensor_name, val_dict):
        return True

    def get_type(self):
        return self.device_type

    def get_meta_id(self, version='1'):
        return '%s-%s' % (self.get_type(), version)

    def get_sensor_meta_id(self, sensor_name, val_dict):
        sensor_def = self.get_sensor_def(sensor_name)
        if 'meta_id' not in sensor_def:
            return 'unknown'
        return sensor_def['meta_id']

    def get_sensor_defs(self):
        log.error('No Sensor Defs defined for base class Device')
        return None

    def get_sensor_def(self, sensor_name):
        sensor_defs = self.get_sensor_defs()
        if sensor_name not in sensor_defs:
            return None
        return sensor_defs[sensor_name]

    # Get raw value or list of values
    def get_raw_value(self, name, val_dict):
        log.error('No get_raw_value defined for base class Device')
        return None

    def check_value(self, name, val_dict, value=None):
        log.error('No check_value defined for base class Device')
        return None

    # Get location as lon, lat
    def get_lon_lat(self, val_dict):
        return None, None
