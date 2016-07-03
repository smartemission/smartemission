from sensorconverters import *

# Allowed min/max values for sensor-names
# See e.g. http://whale.citygis.nl//sensors/v1/devices/20
# TODO apply before conversion i.s.o. ad-hoc checks, even better one generic dict with all sensor metadata
#
RAW_RANGE_FILTERS = {
    # outputs: [
    # {

}
# All sensor definitions, both base sensors (Jose) and derived (virtual) sensors
# Jose sensor defs have id starting with s_ or v_
SENSOR_DEFS = {
    # START GPS Jose
    's_altimeter':
        {
            'label': 'Height',
            'unit': 'Meter',
            'min': 0,
            'max': 4000
        },
    # START Light Jose
    's_lightsensortop':
        {
            'label': 'Light Top',
            'unit': 'Lux',
            'min': 0,
            'max': 65535
        },
    's_lightsensorbottom':
        {
            'label': 'Light Bottom',
            'unit': 'Lux',
            'min': 0,
            'max': 65535
        },
    's_lightsensorred':
        {
            'label': 'Red Light',
            'unit': 'Lux',
            'min': 0,
            'max': 65535
        },
    's_lightsensorgreen':
        {
            'label': 'Green Light',
            'unit': 'Lux',
            'min': 0,
            'max': 65535
        },
    's_lightsensorblue':
        {
            'label': 'Blue Light',
            'unit': 'Lux',
            'min': 0,
            'max': 65535
        },
    's_rgbcolor':
        {
            'label': 'RGB Light',
            'unit': 'RGB8',
            'min': 0,
            'max': 16777215
        },
    # START Accelometer Jose
    's_accelerox':
        {
            'label': 'Acceleration in the X-axis',
            'unit': 'oG',
            'min': 0,
            'max': 1024
        },
    's_acceleroy':
        {
            'label': 'Acceleration in the Y-axis',
            'unit': 'oG',
            'min': 0,
            'max': 1024
        },
    's_acceleroz':
        {
            'label': 'Acceleration in the Z-axis',
            'unit': 'oG',
            'min': 0,
            'max': 1024
        },
    # START Diverse Jose
    's_bottomswitches':
        {
            'label': 'Bottom Switches',
            'unit': '?',
            'min': 0,
            'max': 3
        },
    # START Gasses Jose
    's_o3resistance':
        {
            'id': 23,
            'label': 'O3Raw',
            'unit': 'Ohm',
            'min': 3000,
            'max': 60000
        },
    's_no2resistance':
        {
            'id': 24,
            'label': 'NO2RawOhm',
            'unit': 'Ohm',
            'min': 800,
            'max': 20000
        },
    's_coresistance':
        {
            'id': 25,
            'label': 'CORawOhm',
            'unit': 'Ohm',
            'min': 100000,
            'max': 1500000
        },
    's_co':
        {
            'label': 'CO Concentration',
            'unit': 'ppb',
            'min': 0,
            'max': 1000
        },
    's_no2':
        {
            'label': 'NO2 Concentration',
            'unit': 'ppb',
            'min': 50,
            'max': 1000
        },
    's_o3':
        {
            'label': 'O3 Concentration',
            'unit': 'ppb',
            'min': 10,
            'max': 1000
        },
    's_co2':
        {
            'label': 'CO2 Concentration',
            'unit': 'ppb',
            'min': 0,
            'max': 5000000
        },
    # START particles Jose
    's_pm10':
        {
            'label': 'PM 10',

            'unit': 'ng/m3',
            'min': 0,
            'max': 80000
        },
    's_pm2_5':
        {
            'label': 'PM 2.5',
            'unit': 'ng/m3',
            'min': 0,
            'max': 80000
        },
    's_pm1':
        {
            'label': 'PM 1',
            'unit': 'ng/m3',
            'min': 0,
            'max': 80000
        },
    's_tsp':
        {
            'label': 'Total Suspended Particles',
            'unit': 'ng/m3',
            'min': 0,
            'max': 80000
        },
    # START Meteo Jose
    's_temperatureunit':
        {
            'label': 'Unit Temperature',
            'unit': 'milliKelvin',
            'min': 233150,
            'max': 398150
        },
    's_temperatureambient':
        {
            'id': 5,
            'label': 'Temperatuur',
            'unit': 'milliKelvin',
            'min': 233150,
            'max': 398150
        },
    's_barometer':
        {
            'id': 6,
            'label': 'Luchtdruk',
            'unit': 'HectoPascal',
            'min': 20000,
            'max': 110000

        },
    's_humidity':
        {
            'id': 7,
            'label': 'Relative Humidity',
            'unit': 'm%RH',
            'min': 20000,
            'max': 100000
        },
    's_rain':
        {
            'label': 'Rain',
            'unit': 'Rain value',
            'min': 0,
            'max': 15
        },
    's_externaltemp':
        {
            'label': 'External Temperature',
            'unit': 'milliKelvin',
            'min': 233150,
            'max': 398150
        },
    's_windspeed':
        {
            'label': 'Wind Speed',
            'unit': 'mm/s',
            'min': 0,
            'max': 200000
        },
    's_windheading':
        {
            'label': 'Wind Heading',

            'unit': 'mDegrees',
            'min': 0,
            'max': 360000
        },
    # START Audio Jose
    'v_audio0':
        {
            'id': 8,
            'label': 'Audio 0-40Hz',
            'unit': 'dB(A)'
        },
    'v_audioplus1':
        {
            'id': 9,
            'label': 'Audio 40-80Hz',
            'unit': 'dB(A)'
        },
    'v_audioplus2':
        {
            'id': 10,
            'label': 'Audio 80-160Hz',
            'unit': 'dB(A)'
        },
    'v_audioplus3':
        {
            'id': 11,
            'label': 'Audio 160-315Hz',
            'unit': 'dB(A)'
        },
    'v_audioplus4':
        {
            'id': 12,
            'label': 'Audio 315-630Hz',
            'unit': 'dB(A)'
        },
    'v_audioplus5':
        {
            'id': 13,
            'label': 'Audio 630Hz-1.25kHz',
            'unit': 'dB(A)'
        },
    'v_audioplus6':
        {
            'id': 14,
            'label': 'Audio 1.25-2.5kHz',
            'unit': 'dB(A)'
        },
    'v_audioplus7':
        {
            'id': 15,
            'label': 'Audio 2.5-5kHz',
            'unit': 'dB(A)'
        },
    'v_audioplus8':
        {
            'id': 16,
            'label': 'Audio 5-10kHz',
            'unit': 'dB(A)'
        },
    'v_audioplus9':
        {
            'id': 17,
            'label': 'Audio 10-20kHz',
            'unit': 'dB(A)'
        },
    'v_audioplus10':
        {
            'id': 18,
            'label': 'Audio 20-25kHz',
            'unit': 'dB(A)'
        },
    # START user-defined Sensors
    'temperature':
        {
            'id': 100,
            'label': 'Temperatuur',
            'unit': 'Celsius',
            'input': 's_temperatureambient',
            'converter': convert_temperature,
            'type': int,
            'min': -25,
            'max': 60
        },
    'pressure':
        {
            'id': 101,
            'label': 'Luchtdruk',
            'unit': 'HectoPascal',
            'input': 's_barometer',
            'converter': convert_barometer,
            'type': int,
            'min': 200,
            'max': 1100
        },
    'humidity':
        {
            'id': 103,
            'label': 'Luchtvochtigheid',
            'unit': 'Procent',
            'input': 's_humidity',
            'converter': convert_humidity,
            'type': int,
            'min': 20,
            'max': 100
        },
    'noiseavg':
        {
            'id': 104,
            'label': 'Average Noise',
            'unit': 'dB(A)',
            'input': ['v_audio0', 'v_audioplus1', 'v_audioplus2', 'v_audioplus3', 'v_audioplus4', 'v_audioplus5',
                      'v_audioplus6', 'v_audioplus7', 'v_audioplus8', 'v_audioplus9', 'v_audioplus10'],
            'converter': convert_audio_avg,
            'type': int
        },
    'noiselevelavg':
        {
            'id': 1055,
            'label': 'Average Noise Level 1-5',
            'unit': 'int',
            'input': 'noiseavg',
            'converter': convert_noise_level,
            'type': int
        },
    'co2':
        {
            'id': 106,
            'label': 'CO2',
            'unit': 'ppm',
            'input': 's_co2',
            'converter': ppb_co2_to_ppm,
            'type': int,
            'min': 0,
            'max': 5000
        },
    'coraw':
        {
            'id': 107,
            'label': 'CORaw',
            'unit': 'kOhm',
            'input': ['s_coresistance'],
            'min': 100,
            'max': 1500,
            'converter': ohm_to_kohm
        },
    #     'co':
    # {
    #     'id': 7,
    #     'label': 'CO',
    #     'unit': 'ug/m3'
    # },
    'no2raw':
        {
            'id': 108,
            'label': 'NO2Raw',
            'unit': 'kOhm',
            'input': ['s_no2resistance'],
            'min': 8,
            'max': 2000,
            'converter': ohm_to_kohm
        },
    #     'co':
    # {
    #     'no2',
    #     'id': 8,
    #     'label': 'NO2',
    #     'unit': 'ug/m3'
    # },
    'o3raw':
        {
            'id': 109,
            'label': 'O3Raw',
            'unit': 'kOhm',
            'input': ['s_o3resistance'],
            'min': 3,
            'max': 60,
            'converter': ohm_to_kohm
        },
    'o3':
        {
            'id': 110,
            'label': 'O3',
            'unit': 'ug/m3',
            'input': ['s_o3resistance', 's_no2resistance', 's_coresistance', 's_temperatureambient',
                      's_temperatureunit', 's_humidity', 's_barometer', 's_lightsensorbottom'],
            'converter': ohm_o3_to_ugm3,
            'type': int,
            'min': 0,
            'max': 400
        }
}


# Get raw value or list of values
def get_raw_value(name, val_dict):
    val = None
    if type(name) is list:
        return get_raw_value(name[0], val_dict)
        # name is list of names
        # for n in name:
        #     if n in val_dict:
        #         if val is None:
        #             val = []
        #         val.append(val_dict[n])
    else:
        # name is single name
        if name in val_dict:
            val = val_dict[name]

    return val


# Check for valid input
def check_value(name, val_dict, value=None):
    val = None
    if type(name) is list:
        # name is list of names
        for n in name:
            result, reason = check_value(n, val_dict, value)
            if result is False:
                return result, reason
    else:
        # name is single name
        if name not in val_dict and value is None:
            return False, '%s not present' % name
        else:
            if value is not None:
                val = value
            else:
                val = val_dict[name]

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
