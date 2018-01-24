import math
import re

from smartem.util.utc import zulu_to_gmt

# Conversion functions for raw values from Josene sensors

# Zie http://www.apis.ac.uk/unit-conversion
# ug/m3 = PPB * moleculair gewicht/moleculair volume
# waar molec vol = 22.41 * T/273 * 1013/P
#
# Typische waarden:
# Nitrogen dioxide 1 ppb = 1.91 ug/m3  bij 10C 1.98, bij 30C 1.85 --> 1.9
# Ozone 1 ppb = 2.0 ug/m3  bij 10C 2.1, bij 30C 1.93 --> 2.0
# Carbon monoxide 1 ppb = 1.16 ug/m3 bij 10C 1.2, bij 30C 1.1 --> 1.15
#
# Benzene 1 ppb = 3.24 ug/m3
# Sulphur dioxide 1 ppb = 2.66 ug/m3
# For now a crude approximation as the measurements themselves are also not very accurate
# For now a crude conversion (1 atm, 20C)


def convert_temperature(input, json_obj=None, sensor_def=None):
    if input == 0:
        return None

    tempC = float(input) / 1000.0 - 273.1
    if tempC > 100 or tempC < -40:
        return None

    return tempC

def convert_barometer(input, json_obj=None, sensor_def=None):
    result = float(input) / 100.0
    if result > 1100.0:
        return None
    return result


def convert_humidity(input, json_obj=None, sensor_def=None):
    humPercent = float(input) / 1000.0
    if humPercent > 100:
        return None
    return humPercent


def convert_timestamp(input, json_obj=None, sensor_def=None):
    # input: 2016-05-31T15:55:33.2014241Z
    # iso_str : '2016-05-31T15:55:33GMT'
    return zulu_to_gmt(input)


def convert_none(value, json_obj=None, sensor_def=None):
    return value

