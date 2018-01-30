# -*- coding: utf-8 -*-
#
# AirSensEUR ('ase') Device implementation.
#
# Author: Just van den Broecke - 2018

import logging
from device import Device
from airsenseurdefs import SENSOR_DEFS

log = logging.getLogger('AirSensEURDevice')


class AirSensEUR(Device):

    def __init__(self):
        Device.__init__(self, 'ase')
        self.config_dict = None

    def init(self, config_dict):

        self.config_dict = config_dict

    def exit(self):
        pass

    def can_resolve(self, sensor_name, val_dict):
        sensor_def = self.get_sensor_def(sensor_name)
        if not sensor_def:
            return False

        if 'input' not in sensor_def:
            # Last input in chain
            return sensor_name == val_dict['name']

        input_list = sensor_def['input']
        if type(input_list) is str:
            input_list = [input_list]
            
        result = True
        for input_name in input_list:
            if not self.can_resolve(input_name, val_dict):
                result = False
                break

        return result

    def get_sensor_defs(self):
        return SENSOR_DEFS

    def get_sensor_meta_id(self, sensor_name, val_dict):
        sensor_def = self.get_sensor_def(sensor_name)
        meta_id = 'unknown'
        if 'meta_id' not in sensor_def:
            input_list = sensor_def['input']
            for input_name in input_list:
                val, name = self.get_raw_value(input_name, val_dict)
                if val:
                    meta_id = self.get_sensor_meta_id(input_name, val_dict)
                    break
        else:
            meta_id = sensor_def['meta_id']
        return meta_id

    # Get raw sensor value or list of values
    def get_raw_value(self, name, val_dict):
        val = None
        if type(name) is list:
            for n in name:
                val, n = self.get_raw_value(n, val_dict)
                if val:
                    name = n
                    break
        else:
            # name is single name
            if name == val_dict['name']:
                val = val_dict['sampleEvaluatedVal']

        return val, name

    # Check for valid sensor value
    def check_value(self, name, val_dict, value=None):
        val = None
        if type(name) is list:
            # name is list of names, one of them needs to be available
            for n in name:
                result, reason = self.check_value(n, val_dict, value)
                if result is True:
                    break
        else:
            # name is single name
            if name != val_dict['name'] and value is None:
                return False, '%s not present' % name
            else:
                if value is not None:
                    val = value
                else:
                    val = val_dict['sampleEvaluatedVal']

                if val is None:
                    return False, '%s is None' % name

                if name not in SENSOR_DEFS:
                    return False, '%s not in SENSOR_DEFS' % name

                name_def = SENSOR_DEFS[name]

                if 'min' in name_def and val < name_def['min']:
                    return False, '%s: val(%s) < min(%s)' % (name, str(val), str(name_def['min']))

                if 'max' in name_def and val > name_def['max']:
                    return False, '%s: val(%s) > max(%s)' % (name, str(val), str(name_def['max']))

        return True, '%s OK' % name

    # Get location as lon, lat
    def get_lon_lat(self, val_dict):
        lon = None
        lat = None
        if 'longitude' in val_dict:
            lon = val_dict['longitude']
            if lon < -90.0 or lon > 90.0:
                return None, None

        if 'latitude' in val_dict:
            lat = val_dict['latitude']
            if lat < -180.0 or lat > 180.0:
                return None, None

        return lon, lat
