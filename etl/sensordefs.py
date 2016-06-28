# Outputs to be gathered, with some metadata
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
    # Virtual outputs, i.e. added here for ease of interpretation
    {
        'name': 'v_audioavg',
        'id': 19,
        'label': 'Audio Average Value',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audiolevel',
        'id': 22,
        'label': 'Average Audio/Noise Level 1-5',
        'unit': 'int'
    },
    # {
    #     'name': 's_co',
    #     'id': 1,
    #     'label': 'CO',
    #     'unit': 'ug/m3'
    # },
    {
        'name': 's_co2',
        'id': 2,
        'label': 'CO2',
        'unit': 'ppm'
    },
    # {
    #     'name': 's_no2',
    #     'id': 3,
    #     'label': 'NO2',
    #     'unit': 'ug/m3'
    # },
    {
        'name': 's_o3',
        'id': 4,
        'label': 'O3',
        'unit': 'ug/m3'
    }
]

# Outputs to be gathered, with some metadata
OUTPUTS = [
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
    # Virtual outputs, i.e. added here for ease of interpretation
    {
        'name': 'v_audioavg',
        'id': 19,
        'label': 'Audio Average Value',
        'unit': 'dB(A)'
    },
    {
        'name': 'v_audiolevel',
        'id': 22,
        'label': 'Average Audio/Noise Level 1-5',
        'unit': 'int'
    },
    # {
    #     'name': 's_co',
    #     'id': 1,
    #     'label': 'CO',
    #     'unit': 'ug/m3'
    # },
    {
        'name': 's_co2',
        'id': 2,
        'label': 'CO2',
        'unit': 'ppm'
    },
    # {
    #     'name': 's_no2',
    #     'id': 3,
    #     'label': 'NO2',
    #     'unit': 'ug/m3'
    # },
    {
        'name': 's_o3',
        'id': 4,
        'label': 'O3',
        'unit': 'ug/m3'
    }
]
