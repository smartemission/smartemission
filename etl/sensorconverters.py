import time
from calendar import timegm
from datetime import datetime, tzinfo, timedelta
import re
import math
# from stetl.util import Util
from os import sys, path

import picklegit
import numpy as np

# Make absolute location for pickled calibration objects
file_dir = path.dirname(path.abspath(__file__))

pipeline_objects = {'co': path.join(file_dir, 'calibration/model/pipeline_co.pkl'),
                    'no2': path.join(file_dir, 'calibration/model/pipeline_no2.pkl'),
                    'o3': path.join(file_dir, 'calibration/model/pipeline_o3.pkl')}
running_mean_param = {'co': {'co': 0.005, 'no2': 0.005, 'o3': 0.005},
                      'no2': {'co': 0.005, 'no2': 0.005, 'o3': 0.005},
                      'o3': {'co': 0.005, 'no2': 0.005, 'o3': 0.005}}
running_means = {'co': {'co': None, 'no2': None, 'o3': None},
                 'no2': {'co': None, 'no2': None, 'o3': None},
                 'o3': {'co': None, 'no2': None, 'o3': None}}

# log = Util.get_log("SensorConverters")

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
def ppb_to_ugm3(component, input):
    ppb_to_ugm3_factor = {'o3': 2.0, 'no2': 1.9, 'co': 1.15, 'co2': 1.8}
    if input == 0 or input > 1000000 or component not in ppb_to_ugm3_factor:
        return None

    return ppb_to_ugm3_factor[component] * float(input)


def ppb_co_to_ugm3(input, json_obj, sensor_def):
    return ppb_to_ugm3('co', input)


def ppb_co2_to_ugm3(input, json_obj, sensor_def):
    return ppb_to_ugm3('co2', input)


def ppb_co2_to_ppm(input, json_obj, sensor_def):
    return input / 1000.0


def ppb_no2_to_ugm3(input, json_obj, sensor_def):
    return ppb_to_ugm3('no2', input)


def ppb_o3_to_ugm3(input, json_obj, sensor_def):
    return input


def running_mean(previous_val, new_val, alpha):
    if new_val is None:
        return previous_val

    if previous_val is None:
        previous_val = new_val
    val = new_val * alpha + previous_val * (1.0 - alpha)
    return val


def ohm_co_to_ugm3(input, json_obj, sensor_def):
    global running_means

    val = None

    # Original value in kOhm
    s_o3resistance = ohm_to_kohm(json_obj['s_o3resistance'])
    s_no2resistance = ohm_no2_to_kohm(json_obj['s_no2resistance'])
    s_coresistance = ohm_to_kohm(json_obj['s_coresistance'])
    s_temperatureambient = convert_temperature(json_obj['s_temperatureambient'])
    s_temperatureunit = convert_temperature(json_obj['s_temperatureunit'])
    s_humidity = convert_humidity(json_obj['s_humidity'])
    s_barometer = convert_barometer(json_obj['s_barometer'])

    # Filter value
    co_running_means = running_means['co']
    co_running_means_param = running_mean_param['co']
    co_running_means['co'] = running_mean(co_running_means['co'], s_coresistance, co_running_means_param['co'])
    co_running_means['no2'] = running_mean(co_running_means['no2'], s_no2resistance, co_running_means_param['no2'])
    co_running_means['o3'] = running_mean(co_running_means['o3'], s_o3resistance, co_running_means_param['o3'])

    # Predict RIVM value
    value_array = np.array([s_barometer, s_humidity, s_temperatureambient, s_temperatureunit, co_running_means['co'],
                        co_running_means['no2'], co_running_means['o3']]).reshape(1, -1)
    with open(pipeline_objects['co'], 'rb') as f:
        co_pipeline = pickle.load(f)
    val = co_pipeline.predict(value_array)

    return val[0]


def ohm_no2_to_ugm3(input, json_obj, sensor_def):
    global running_means

    val = None

    # Original value in kOhm
    s_o3resistance = ohm_to_kohm(json_obj['s_o3resistance'])
    s_no2resistance = ohm_no2_to_kohm(json_obj['s_no2resistance'])
    s_coresistance = ohm_to_kohm(json_obj['s_coresistance'])
    s_temperatureambient = convert_temperature(json_obj['s_temperatureambient'])
    s_temperatureunit = convert_temperature(json_obj['s_temperatureunit'])
    s_humidity = convert_humidity(json_obj['s_humidity'])
    s_barometer = convert_barometer(json_obj['s_barometer'])

    # Filter value
    no2_running_means = running_means['no2']
    no2_running_means_param = running_mean_param['no2']
    no2_running_means['co'] = running_mean(no2_running_means['co'], s_coresistance, no2_running_means_param['co'])
    no2_running_means['no2'] = running_mean(no2_running_means['no2'], s_no2resistance, no2_running_means_param['no2'])
    no2_running_means['o3'] = running_mean(no2_running_means['o3'], s_o3resistance, no2_running_means_param['o3'])

    # Predict RIVM value
    value_array = np.array([s_barometer, s_humidity, s_temperatureambient, s_temperatureunit, no2_running_means['co'],
                        no2_running_means['no2'], no2_running_means['o3']]).reshape(1, -1)
    with open(pipeline_objects['no2'], 'rb') as f:
        no2_pipeline = pickle.load(f)
    val = no2_pipeline.predict(value_array)

    return val[0]


# http://smartplatform.readthedocs.io/en/latest/data.html#o3-calibration
def ohm_o3_to_ugm3(input, json_obj, sensor_def):
    global running_means

    val = None

    # Original value in kOhm
    s_o3resistance = ohm_to_kohm(json_obj['s_o3resistance'])
    s_no2resistance = ohm_no2_to_kohm(json_obj['s_no2resistance'])
    s_coresistance = ohm_to_kohm(json_obj['s_coresistance'])
    s_temperatureambient = convert_temperature(json_obj['s_temperatureambient'])
    s_temperatureunit = convert_temperature(json_obj['s_temperatureunit'])
    s_humidity = convert_humidity(json_obj['s_humidity'])
    s_barometer = convert_barometer(json_obj['s_barometer'])

    # Filter value
    o3_running_means = running_means['o3']
    o3_running_means_param = running_mean_param['o3']
    o3_running_means['co'] = running_mean(o3_running_means['co'], s_coresistance, o3_running_means_param['co'])
    o3_running_means['no2'] = running_mean(o3_running_means['no2'], s_no2resistance, o3_running_means_param['no2'])
    o3_running_means['o3'] = running_mean(o3_running_means['o3'], s_o3resistance, o3_running_means_param['o3'])

    # Predict RIVM value
    value_array = np.array([s_barometer, s_humidity, s_temperatureambient, s_temperatureunit, o3_running_means['co'],
                            o3_running_means['no2'], o3_running_means['o3']]).reshape(1, -1)
    with open(pipeline_objects['o3'], 'rb') as f:
        # s = f.read()
        o3_pipeline = pickle.load(f)

    val = o3_pipeline.predict(value_array)

    # log.info('device: %d : O3 : ohm=%d ugm3=%d' % (device, input, val))
    return val[0]


def ohm_to_kohm(input, json_obj=None, sensor_def=None):
    return float(input) / 1000.0


def ohm_no2_to_kohm(input, json_obj=None, sensor_def=None):
    val = ohm_to_kohm(input, json_obj, sensor_def)
    if val > 2000:
        return None
    return val


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


# Lat or longitude conversion
# 8 nibbles:
# MSB                  LSB
# n1 n2 n3 n4 n5 n6 n7 n8
# n1: 0 of 8, 0=East/North, 8=West/South
# n2 en n3: whole degrees (0-180)
# n4-n8: fraction of degrees (max 999999)
def convert_coord(input, json_obj=None, sensor_def=None):
    sign = 1.0
    if input >> 28:
        sign = -1.0
    deg = float((input >> 20) & 255)
    dec = float(input & 1048575)

    result = (deg + dec / 1000000.0) * sign
    if result == 0.0:
        result = None
    return result


def convert_latitude(input, json_obj, sensor_def):
    res = convert_coord(input)
    if res is not None and (res < -90.0 or res > 90.0):
        # log.error('Invalid latitude device=%d : %d' % (json_obj['p_unitserialnumber'], res))
        return None
    return res


def convert_longitude(input, json_obj, sensor_def):
    res = convert_coord(input)
    if res is not None and (res < -180.0 or res > 180.0):
        # log.error('Invalid longitude device=%d : %d' % (json_obj['p_unitserialnumber'], res))
        return None
    return res

# https://aboutsimon.com/blog/2013/06/06/Datetime-hell-Time-zone-aware-to-UNIX-timestamp.html
# Somehow need to force timezone in....TODO: may use dateutil external package
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)

utc = UTC()


def convert_timestamp(input, json_obj=None, sensor_def=None):
    # input: 2016-05-31T15:55:33.2014241Z
    # iso_str : '2016-05-31T15:55:33GMT'
    iso_str = input.split('.')[0] + 'GMT'
    # timestamp = timegm(
    #         time.strptime(iso_str, '%Y-%m-%dT%H:%M:%SGMT')
    # )
    # print timestamp
    # print '-> %s' % datetime.utcfromtimestamp(timestamp).isoformat()

    return datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SGMT').replace(tzinfo=utc)


def convert_none(value, json_obj=None, sensor_def=None):
    return value


# From https://www.teachengineering.org/view_activity.php?url=collection/nyu_/activities/nyu_noise/nyu_noise_activity1.xml
# level dB(A)
#  1     0-20  zero to quiet room
#  2     20-40 up to average residence
#  3     40-80 up to noisy class, alarm clock, police whistle
#  4     80-90 truck with muffler
#  5     90-up severe: pneumatic drill, artillery,
#
# Peter vd Voorn:
# Voor het categoriseren van de meetwaarden kunnen we het beste beginnen bij de 20 dB(A).
# De hoogte waarde zal 95 dB(A) zijn. Bijvoorbeeld een vogel van heel dichtbij.
# Je kunt dit nu gewoon lineair verdelen in 5 categorieen. Ieder 15 dB. Het betreft buiten meetwaarden.
# 20 fluister stil
# 35 rustige woonwijk in een stad
# 50 drukke woonwijk in een stad
# 65 wonen op korte afstand van het spoor
# 80 live optreden van een band aan het einde van het publieksdeel. Praten is mogelijk.
# 95 live optreden van een band midden op een plein. Praten is onmogelijk.
def calc_audio_level(db):
    levels = [20, 35, 50, 65, 80, 95]
    level_num = 1
    for i in range(0, len(levels)):
        if db > levels[i]:
            level_num = i + 1

    return level_num

def convert_noise_level(value, json_obj, sensor_def):
    return calc_audio_level(value)

# Converts audio var and populates average
# Logaritmisch optellen van de waarden per frequentieband voor het verkrijgen van de totaalwaarde:
#
# 10^(waarde/10)
# En dat voor de waarden van alle frequenties en bij elkaar tellen.
# Daar de log van en x10
#
# Normaal tellen wij op van 31,5 Hz tot 8 kHz. In totaal 9 oktaafanden. 31,5  63  125  250  500  1000  2000  4000 en 8000 Hz
#
# Of 27   1/3 oktaafbanden: 25, 31.5, 40, 50, 63, 80, enz
def convert_noise_avg(value, json_obj, sensor_def):
    # For each audio observation:
    # decode into 3 bands (0,1,2)
    # determine average of these  bands
    # determine overall average of all average bands
    # Extract values for bands 0-2
    input_names = sensor_def['input']
    for input_name in input_names:
        input_value = json_obj[input_name]

        bands = [float(input_value & 255), float((input_value >> 8) & 255), float((input_value >> 16) & 255)]

        # determine average of these 3 bands
        band_avg = 0
        band_cnt = 0
        dbMin = sensor_def['min']
        dbMax = sensor_def['max']
        for i in range(0, len(bands)):
            band_val = bands[i]
            # outliers
            if band_val < dbMin or band_val > dbMax:
                continue
            band_cnt += 1

            # convert band value Decibel to Bel and then get "real" value (power 10)
            band_avg += math.pow(10, band_val / 10)
            # print '%s : band[%d]=%f band_avg=%f' %(name, i, bands[i], band_avg)

        if band_cnt == 0:
            return None

        # Take average of "real" values and convert back to Bel via log10 and Decibel via *10
        band_avg = math.log10(band_avg / float(band_cnt)) * 10.0

        # print '%s : avg=%d' %(name, band_avg)

        if band_avg < dbMin or band_avg > dbMax:
            return None

        # Initialize  average value to first average calc
        if 'noiseavg' not in json_obj:
            json_obj['noiseavg'] = band_avg
            json_obj['noiseavg_total'] = math.pow(10, band_avg / 10)
            json_obj['noiseavg_cnt'] = 1
        else:
            json_obj['noiseavg_cnt'] += 1
            json_obj['noiseavg_total'] += math.pow(10, band_avg / 10)
            json_obj['noiseavg'] = int(
                round(math.log10(json_obj['noiseavg_total'] / json_obj['noiseavg_cnt']) * 10.0))

    # Determine octave nr from var name
    # json_obj['v_audiolevel'] = calc_audio_level(json_obj['v_audioavg'])
    # print 'Unit %s - %s band_db=%f avg_db=%d level=%d' % (json_obj['p_unitserialnumber'], sensor_def, band_avg, json_obj['v_audioavg'], json_obj['v_audiolevel'] )
    return json_obj['noiseavg']

# Converts audio var and populates virtual max value vars
# NB not used: now taking average of max values, see convert_audio_avg()
def convert_audio_max(value, json_obj, sensor_def):
    # For each audio observation:
    # decode into 3 bands (0,1,2)
    # determine max of these  bands
    # determine if this is greater than current t_audiomax
    # determine audio_level (1-5) from current t_audiomax

    # Extract values for bands 0-2
    bands = [value & 255, (value >> 8) & 255, (value >> 16) & 255]

    band_max = 0
    band_num = 0
    for i in range(0, len(bands)):
        if band_max < bands[i] < 255:
            band_max = bands[i]
            band_num = i

    if band_max == 0:
        return None

    # Assign band max value to virtual sensors if these are not yet present
    # or band_max value greater than current max
    if 't_audiomax' not in json_obj or band_max > json_obj['t_audiomax']:
        json_obj['t_audiomax'] = band_max
        # Determine octave nr from var name
        json_obj['t_audiomax_octave'] = int(re.findall(r'\d+', sensor_def['name'])[0])
        json_obj['t_audiomax_octband'] = band_num
        json_obj['t_audiolevel'] = calc_audio_level(band_max)

    return band_max

