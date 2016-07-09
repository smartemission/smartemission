from sensorconverters import *

# According to CityGIS the units are defined as follows. ::
#
# S.TemperatureUnit		milliKelvin
# S.TemperatureAmbient	milliKelvin
# S.Humidity				%mRH
# S.LightsensorTop		Lux
# S.LightsensorBottom		Lux
# S.Barometer				Pascal
# S.Altimeter				Meter
# S.CO					ppb
# S.NO2					ppb
# S.AcceleroX				2 ~ +2G (0x200 = midscale)
# S.AcceleroY				2 ~ +2G (0x200 = midscale)
# S.AcceleroZ				2 ~ +2G (0x200 = midscale)
# S.LightsensorRed		Lux
# S.LightsensorGreen		Lux
# S.LightsensorBlue		Lux
# S.RGBColor				8 bit R, 8 bit G, 8 bit B
# S.BottomSwitches		?
# S.O3					ppb
# S.CO2					ppb
# v3: S.ExternalTemp		milliKelvin
# v3: S.COResistance		Ohm
# v3: S.No2Resistance		Ohm
# v3: S.O3Resistance		Ohm
# S.AudioMinus5			Octave -5 in dB(A)
# S.AudioMinus4			Octave -4 in dB(A)
# S.AudioMinus3			Octave -3 in dB(A)
# S.AudioMinus2			Octave -2 in dB(A)
# S.AudioMinus1			Octave -1 in dB(A)
# S.Audio0				Octave 0 in dB(A)
# S.AudioPlus1			Octave +1 in dB(A)
# S.AudioPlus2			Octave +2 in dB(A)
# S.AudioPlus3			Octave +3 in dB(A)
# S.AudioPlus4			Octave +4 in dB(A)
# S.AudioPlus5			Octave +5 in dB(A)
# S.AudioPlus6			Octave +6 in dB(A)
# S.AudioPlus7			Octave +7 in dB(A)
# S.AudioPlus8			Octave +8 in dB(A)
# S.AudioPlus9			Octave +9 in dB(A)
# S.AudioPlus10			Octave +10 in dB(A)
# S.SatInfo
# S.Latitude				nibbles: n1:0=East/North, 8=West/South; n2&n3: whole degrees (0-180); n4-n8: degree fraction (max 999999)
# S.Longitude				nibbles: n1:0=East/North, 8=West/South; n2&n3: whole degrees (0-180); n4-n8: degree fraction (max 999999)
#
# P.Powerstate					Power State
# P.BatteryVoltage				Battery Voltage (milliVolts)
# P.BatteryTemperature			Battery Temperature (milliKelvin)
# P.BatteryGauge					Get Battery Gauge, BFFF = Battery full, 1FFF = Battery fail, 0000 = No Battery Installed
# P.MuxStatus						Mux Status (0-7=channel,F=inhibited)
# P.ErrorStatus					Error Status (0=OK)
# P.BaseTimer						BaseTimer (seconds)
# P.SessionUptime					Session Uptime (seconds)
# P.TotalUptime					Total Uptime (minutes)
# v3: P.COHeaterMode				CO heater mode
# P.COHeater						Powerstate CO heater (0/1)
# P.NO2Heater						Powerstate NO2 heater (0/1)
# P.O3Heater						Powerstate O3 heater (0/1)
# v3: P.CO2Heater					Powerstate CO2 heater (0/1)
# P.UnitSerialnumber				Serialnumber of unit
# P.TemporarilyEnableDebugLeds	Debug leds (0/1)
# P.TemporarilyEnableBaseTimer	Enable BaseTime (0/1)
# P.ControllerReset				WIFI reset
# P.FirmwareUpdate				Firmware update, reboot to bootloader
#
# Unknown at this moment (decimal):
# P.11
# P.16
# P.17
# P.18

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
    's_latitude':
        {
            'label': 'Latitude Raw',
            'unit': 'int'
        },
    's_longitude':
        {
            'label': 'Longitude Raw',
            'unit': 'int'
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
            'label': 'O3Raw',
            'unit': 'Ohm',
            'min': 3000,
            'max': 6000000
        },
    's_no2resistance':
        {
            'label': 'NO2RawOhm',
            'unit': 'Ohm',
            'min': 800,
            'max': 20000000
        },
    's_coresistance':
        {
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
            'label': 'Temperatuur',
            'unit': 'milliKelvin',
            'min': 233150,
            'max': 398150
        },
    's_barometer':
        {
            'label': 'Luchtdruk',
            'unit': 'HectoPascal',
            'min': 20000,
            'max': 110000

        },
    's_humidity':
        {
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
            'label': 'Audio 0-40Hz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus1':
        {
            'label': 'Audio 40-80Hz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus2':
        {
            'label': 'Audio 80-160Hz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus3':
        {
            'label': 'Audio 160-315Hz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus4':
        {
            'label': 'Audio 315-630Hz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus5':
        {
            'label': 'Audio 630Hz-1.25kHz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus6':
        {
            'label': 'Audio 1.25-2.5kHz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus7':
        {
            'label': 'Audio 2.5-5kHz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus8':
        {
            'label': 'Audio 5-10kHz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus9':
        {
            'label': 'Audio 10-20kHz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    'v_audioplus10':
        {
            'label': 'Audio 20-25kHz',
            'unit': 'dB(A)',
            'min': -100,
            'max': 195
        },
    # START user-defined/derived Sensors
    'altitude': {
        'label': 'Hoogte',
        'unit': 'Meters',
        'input': 's_altitude',
        'converter': convert_none,
        'type': int,
        'min': -200,
        'max': 3000
    },
    'latitude': {
        'label': 'Latitude',
        'unit': 'Degrees',
        'input': 's_latitude',
        'converter': convert_coord,
        'type': float,
        'min': -90,
        'max': 90
    },
    'longitude': {
        'label': 'Longitude',
        'unit': 'Degrees',
        'input': 's_longitude',
        'converter': convert_coord,
        'type': float,
        'min': -180,
        'max': 180
    },
    'temperature':
        {
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
            'label': 'Average Noise',
            'unit': 'dB(A)',
            'input': ['v_audio0', 'v_audioplus1', 'v_audioplus2', 'v_audioplus3', 'v_audioplus4', 'v_audioplus5',
                      'v_audioplus6', 'v_audioplus7', 'v_audioplus8', 'v_audioplus9'],
            'converter': convert_noise_avg,
            'type': int,
            'min': -100,
            'max': 195
        },
    'noiselevelavg':
        {
            'label': 'Average Noise Level 1-5',
            'unit': 'int',
            'input': 'noiseavg',
            'converter': convert_noise_level,
            'type': int,
            'min': 1,
            'max': 5
        },
    'co2':
        {
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
            'label': 'CORaw',
            'unit': 'kOhm',
            'input': ['s_coresistance'],
            'min': 100,
            'max': 1500,
            'converter': ohm_to_kohm
        },
    'co':
        {
            'label': 'CO',
            'unit': 'ug/m3',
            'input': ['s_o3resistance', 's_no2resistance', 's_coresistance', 's_temperatureambient',
                      's_temperatureunit', 's_humidity', 's_barometer', 's_lightsensorbottom'],
            'converter': ohm_co_to_ugm3,
            'type': int,
            'min': 0,
            'max': 4000
        },
    'no2raw':
        {
            'label': 'NO2Raw',
            'unit': 'kOhm',
            'input': ['s_no2resistance'],
            'min': 8,
            'max': 4000,
            'converter': ohm_to_kohm
        },
    'no2':
        {
            'label': 'NO2',
            'unit': 'ug/m3',
            'input': ['s_o3resistance', 's_no2resistance', 's_coresistance', 's_temperatureambient',
                      's_temperatureunit', 's_humidity', 's_barometer', 's_lightsensorbottom'],
            'converter': ohm_no2_to_ugm3,
            'type': int,
            'min': 0,
            'max': 400
        },
    'o3raw':
        {
            'label': 'O3Raw',
            'unit': 'kOhm',
            'input': ['s_o3resistance'],
            'min': 0,
            'max': 20000,
            'converter': ohm_to_kohm
        },
    'o3':
        {
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


# Check for valid sensor value
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

            # AUdio inputs: need to unpack 3 bands and check for decibel vals
            if 'audio' in name:
                bands = [float(val & 255), float((val >> 8) & 255), float((val >> 16) & 255)]

                # determine validity of these 3 bands
                dbMin = name_def['min']
                dbMax = name_def['max']
                for i in range(0, len(bands)):
                    band_val = bands[i]
                    # outliers
                    if band_val < dbMin:
                        return False, '%s: val(%s) < min(%s)' % (name, str(band_val), str(name_def['min']))
                    elif band_val > dbMax:
                        return False, '%s: val(%s) > max(%s)' % (name, str(band_val), str(name_def['max']))

                return True, '%s OK' % name

            if 'min' in name_def and val < name_def['min']:
                return False, '%s: val(%s) < min(%s)' % (name, str(val), str(name_def['min']))

            if 'max' in name_def and val > name_def['max']:
                return False, '%s: val(%s) > max(%s)' % (name, str(val), str(name_def['max']))

    return True, '%s OK' % name
