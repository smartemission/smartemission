# -*- coding: utf-8 -*-
#
# Device registry: map name to Device instance.
#


# Author: Just van den Broecke - 2015-2018
import logging
from josene import Josene
from airsenseur import AirSensEUR

log = logging.getLogger('DeviceReg')


class DeviceReg:
    """
    Device registry: map name to Device instance.
    """

    devices = {
        'jose': Josene(),
        'ase': AirSensEUR()
    }

    @staticmethod
    def get_device(device_type):
        if device_type not in DeviceReg.devices:
            log.warn('No Device available for device_type=%s' % device_type)
            return None

        return DeviceReg.devices[device_type]
