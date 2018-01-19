# -*- coding: utf-8 -*-
#
# Consume a raw record of Smart Emission data (one hour for one device), refining these, producing records.
#


# Author: Just van den Broecke - 2015-2018
import logging

log = logging.getLogger('Device')


class Device:

    def __init__(self):
        pass

    def init(self, config):
        pass

    def exit(self):
        pass

    def get_sensor_defs(self):
        log.error('No Sensor Defs defined for base class Device')
        return None

    # Get raw value or list of values
    def get_raw_value(self, name, val_dict):
        log.error('No get_raw_value defined for base class Device')
        return None

    def check_value(self, name, val_dict, value=None):
        log.error('No check_value defined for base class Device')
        return None
