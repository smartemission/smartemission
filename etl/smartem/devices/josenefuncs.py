import math
import re

import pandas as pd

from smartem.util.running_mean import RunningMean
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
def ppb_to_ugm3(component, input):
    ppb_to_ugm3_factor = {'o3': 2.0, 'no2': 1.9, 'co': 1.15, 'co2': 1.8}
    if input == 0 or input > 1000000 or component not in ppb_to_ugm3_factor:
        return None

    return ppb_to_ugm3_factor[component] * float(input)


def ppb_co_to_ugm3(input, json_obj=None, sensor_def=None):
    return ppb_to_ugm3('co', input)


def ppb_co2_to_ugm3(input, json_obj=None, sensor_def=None):
    return ppb_to_ugm3('co2', input)


def ppb_co2_to_ppm(input, json_obj=None, sensor_def=None):
    return input / 1000.0


def ppb_no2_to_ugm3(input, json_obj=None, sensor_def=None):
    return ppb_to_ugm3('no2', input)


def ppb_o3_to_ugm3(input, json_obj=None, sensor_def=None):
    return input


def running_mean(previous_val, new_val, alpha):
    if new_val is None:
        return previous_val

    if previous_val is None:
        previous_val = new_val
    val = new_val * alpha + previous_val * (1.0 - alpha)
    return val


def update_running_mean(running_means, alpha, obs):
    for (key, value) in obs.iteritems():
        running_means[key] = running_mean(running_means[key], obs[key], alpha)
    return running_means


def ohm_to_ugm3(input, json_obj, sensor_def):

    # check model specification
    if not ('converter_model' in sensor_def
            and sensor_def['converter_model'] is not None
            and 'mlp_regressor' in sensor_def['converter_model']
            and 'running_mean_weights' in sensor_def['converter_model']
            and 'state' in sensor_def['converter_model']):
        raise ValueError('Converter model not properly specified.')

    # unpack model specification
    converter_model = sensor_def['converter_model']
    mlp_regressor = converter_model['mlp_regressor']
    running_mean_weights = converter_model['running_mean_weights']
    running_mean_state = converter_model['state']

    json_obj['device_id'] = str(json_obj['device_id'])
    if json_obj['device_id'] not in running_mean_state:
        running_mean_state[json_obj['device_id']] = dict()

    val = None

    # filter observations
    state = running_mean_state[json_obj['device_id']]
    for component, weight in running_mean_weights.iteritems():
        if component not in state:
            state[component] = RunningMean(weight)
        json_obj[component] = state[component].observe(json_obj[component])

    # select inputs
    inputs = [json_obj[k] for k in sensor_def['input']]

    # Predict RIVM value if all values are available
    x = pd.DataFrame([inputs])
    val = mlp_regressor.predict(x)[0]

    return val


def ohm_co_to_ugm3(input, json_obj, sensor_def):
    return ohm_to_ugm3(input, json_obj, sensor_def)


def ohm_no2_to_ugm3(input, json_obj, sensor_def):
    return ohm_to_ugm3(input, json_obj, sensor_def)


def ohm_o3_to_ugm3(input, json_obj, sensor_def):
    return ohm_to_ugm3(input, json_obj, sensor_def)


def ohm_to_kohm(input, json_obj=None, sensor_def=None):
    return float(input) / 1000.0


def ohm_no2_to_kohm(input, json_obj=None, sensor_def=None):
    val = ohm_to_kohm(input, json_obj, sensor_def)
    return val

# e.g. for PM10 and PM2_5
def nanogram_to_microgram(input, json_obj=None, sensor_def=None):
    return float(input) / 1000.0


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


def convert_timestamp(input, json_obj=None, sensor_def=None):
    # input: 2016-05-31T15:55:33.2014241Z
    # iso_str : '2016-05-31T15:55:33GMT'
    return zulu_to_gmt(input)


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

# Converts audio var and populates average NB all in dB(A) !
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

        # decode dB(A) values into 3 bands (0,1,2)
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

            # convert band value Decibel(A) to Bel and then get "real" value (power 10)
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
