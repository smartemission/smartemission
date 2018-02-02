#
# Conversion functions for raw values from ASE-based sensors
#
#
# References:
# [1] "Evaluation of low-cost sensors for air pollution monitoring"
# by Spinelle, L., Gerboles, M., Kotsev, A. and Signorini, M. (2017)
# Technical report by the Joint Research Centre (JRC), the European
# Commission's science and knowledge service.
# JRC106095 EUR 28601 EN
#
# [2] https://www.samenmetenaanluchtkwaliteit.nl/sites/default/files/2017-12/Jan%20Vonk_AirSensEUR.pptx.pdf
# Jan Vonk - RIVM
#

TWO_POW_16 = 65536.0


# Equation 1: [1] page 3
# V = (Vref - RefAD) + DigitalReading * 2 *  RefAD / 2**16
def bits2millivolt(value, record_in=None, sensor_def=None, device=None):
    """
    Convert (evaluated) bits value to millivolt according to Vref and RefAD ASE formulas.

    :param int value: input value raw 2 byte number 0..65535
    :param dict json_obj: complete record data object
    :param dict sensor_def:
    :param object: the device object:
    :return:
    """
    # e.g. 'NO2-B43F'
    sensor_name = record_in['name']
    input_names = sensor_def['input']
    if sensor_name not in input_names:
        return None

    input_def = device.get_sensor_def(sensor_name)
    params = input_def['params']
    v_ref = params['v_ref']
    v_ref_ad = params['v_ref_ad']

    # V = (Vref - RefAD) + value * 2 *  RefAD / 2**16
    return ((v_ref - v_ref_ad) + value * 2.0 * v_ref_ad / TWO_POW_16) * 1000.0
