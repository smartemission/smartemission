from smartem.util.utc import zulu_to_gmt

# Generic conversion functions for all sensors.


def convert_none(value, record_in=None, sensor_def=None, device=None):
    """
    Null operation: no conversion.
    
    :param value: input value
    :param record_in: input record (unused)
    :param sensor_def: sensor definition (unused)
    :param device: device object (unused)
    :return: 
    """
    return value


def convert_zulu_to_gmt(input, json_obj=None, sensor_def=None, device=None):
    """
    Convert Zulu time string to GMT time string.
    :param input: Zulu time string, e.g. input: 2016-05-31T15:55:33.2014241Z
    :param json_obj:
    :param sensor_def:
    :param device:
    :return: iso GMT str e.g. '2016-05-31T15:55:33GMT'
    """
    return zulu_to_gmt(input)


def ohm_to_kohm(input, json_obj=None, sensor_def=None, device=None):
    return float(input) / 1000.0


def ppb_to_ppm(input, json_obj=None, sensor_def=None, device=None):
    return input / 1000.0


# e.g. for PM10 and PM2_5
def nanogram_to_microgram(input, json_obj=None, sensor_def=None, device=None):
    return float(input) / 1000.0


# Generic chemical conversions for ppb to ug/m3.
#
# See http://www.apis.ac.uk/unit-conversion
# ug/m3 = PPB * molecular weight/molecular volume
# where molecular volume = 22.41 * T/273 * 1013/P
#
# Typical values:
# Nitrogen dioxide 1 ppb = 1.91 ug/m3  bij 10C 1.98, bij 30C 1.85 --> 1.9
# Ozone 1 ppb = 2.0 ug/m3  bij 10C 2.1, bij 30C 1.93 --> 2.0
# Carbon monoxide 1 ppb = 1.16 ug/m3 bij 10C 1.2, bij 30C 1.1 --> 1.15
#
# Benzene 1 ppb = 3.24 ug/m3
# Sulphur dioxide 1 ppb = 2.66 ug/m3
# For now a crude approximation as the measurements themselves are also not very accurate
# For now a crude conversion (1 atm, 20C)

# Using these generic conversion factors for direct ppb to ug/m3
PPB_TO_UGM3_FACTOR = {
    'o3': 2.0,
    'no2': 1.9,
    'co': 1.15,
    'co2': 1.8
}


def ppb_to_ugm3(component, input):
    if input == 0 or input > 1000000 or component not in PPB_TO_UGM3_FACTOR:
        return None

    return PPB_TO_UGM3_FACTOR[component] * float(input)


def ppb_co_to_ugm3(input, json_obj=None, sensor_def=None, device=None):
    return ppb_to_ugm3('co', input)


def ppb_co2_to_ugm3(input, json_obj=None, sensor_def=None, device=None):
    return ppb_to_ugm3('co2', input)


def ppb_no2_to_ugm3(input, json_obj=None, sensor_def=None, device=None):
    return ppb_to_ugm3('no2', input)


def ppb_o3_to_ugm3(input, json_obj=None, sensor_def=None, device=None):
    return input
