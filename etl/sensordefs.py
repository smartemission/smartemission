from sensorconverters import *

# Inputs from raw sensor
INPUTS = [
    {
        'name': 's_o3resistance',
        'id': 23,
        'label': 'O3Raw',
        'unit': 'kOhm'
    },
    {
        'name': 's_no2resistance',
        'id': 24,
        'label': 'NO2',
        'unit': 'kOhm'
    },
    {
        'name': 's_coresistance',
        'id': 25,
        'label': 'CO',
        'unit': 'kOhm'
    },
    {
        'name': 's_temperatureambient',
        'id': 5,
        'label': 'Temperatuur',
        'unit': 'Celsius'
    },
    {
        'name': 's_barometer',
        'id': 6,
        'label': 'Luchtdruk',
        'unit': 'HectoPascal'
    },
    {
        'name': 's_humidity',
        'id': 7,
        'label': 'Luchtvochtigheid',
        'unit': 'Procent'
    },
    {
        'name': 'v_audio0',
        'id': 8,
        'label': 'Audio 0-40Hz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus1',
        'id': 9,
        'label': 'Audio 40-80Hz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus2',
        'id': 10,
        'label': 'Audio 80-160Hz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus3',
        'id': 11,
        'label': 'Audio 160-315Hz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus4',
        'id': 12,
        'label': 'Audio 315-630Hz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus5',
        'id': 13,
        'label': 'Audio 630Hz-1.25kHz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus6',
        'id': 14,
        'label': 'Audio 1.25-2.5kHz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus7',
        'id': 15,
        'label': 'Audio 2.5-5kHz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus8',
        'id': 16,
        'label': 'Audio 5-10kHz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus9',
        'id': 17,
        'label': 'Audio 10-20kHz',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audioplus10',
        'id': 18,
        'label': 'Audio 20-25kHz',
        'unit': 'dB(A)'
    },
    # Virtual inputs, i.e. added here for ease of interpretation
    {
        'name': 'noiselevel',
        'id': 22,
        'label': 'Average Noise Level 1-5',
        'unit': 'int'
    }
]

# Outputs to be gathered, with some metadata
OUTPUTS = [
    {
        'name': 'temperature',
        'id': 1,
        'label': 'Temperatuur',
        'unit': 'Celsius',
        'input': 's_temperatureambient',
        'converter': convert_temperature,
        'type': int
    },
    {
        'name': 'pressure',
        'id': 2,
        'label': 'Luchtdruk',
        'unit': 'HectoPascal',
        'input': 's_barometer',
        'converter': convert_barometer,
        'type': int
    },
    {
        'name': 'humidity',
        'id': 3,
        'label': 'Luchtvochtigheid',
        'unit': 'Procent',
        'input': 's_humidity',
        'converter': convert_humidity,
        'type': int
    },
    {
        'name': 'noiseavg',
        'id': 4,
        'label': 'Average Noise',
        'unit': 'dB(A)',
        'input': 'v_audio0,v_audioplus1,v_audioplus2,v_audioplus3,v_audioplus4,v_audioplus5,v_audioplus6,v_audioplus7,v_audioplus8,v_audioplus9,v_audioplus10',
        'converter': convert_audio_avg,
        'type': int
    },
    {
        'name': 'noiselevelavg',
        'id': 5,
        'label': 'Average Noise Level 1-5',
        'unit': 'int',
        'input': 'noiseavg',
        'converter': convert_noise_level,
        'type': int
    },
    {
        'name': 'co2',
        'id': 6,
        'label': 'CO2',
        'unit': 'ppm',
        'input': 's_co2',
        'converter': ppb_co2_to_ppm,
        'type': int
    },
    # {
    #     'name': 's_co',
    #     'id': 7,
    #     'label': 'CO',
    #     'unit': 'ug/m3'
    # },
    # {
    #     'name': 's_no2',
    #     'id': 8,
    #     'label': 'NO2',
    #     'unit': 'ug/m3'
    # },
    {
        'name': 'o3',
        'id': 9,
        'label': 'O3',
        'unit': 'ug/m3',
        'input': 's_o3resistance',
        'converter': ohm_o3_to_ugm3,
        'type': int
    }
]


def get_raw_value(name, val_dict):
    val = None
    if ',' not in name:
        if name in val_dict:
            val = val_dict[name]
    else:
        names = name.split(',')
        for n in names:
            if name in val_dict:
                if val is None:
                    val = []
                val.append(val_dict[n])

    return val
