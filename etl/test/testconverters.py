"""
 Naam:         testconverters.py
 Omschrijving: Tests for specifieke conversies
 Auteurs:      Just van den Broecke
"""

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import json
from pprint import pprint
import sensorconverters
from sensordefs import SENSOR_DEFS, check_value, get_raw_value


# Nodig om output naar console/file van strings goed te krijgen
# http://www.saltycrane.com/blog/2008/11/python-unicodeencodeerror-ascii-codec-cant-encode-character/
# anders bijv. deze fout: 'ascii' codec can't encode character u'\xbf' in position 42: ordinal not in range(128)
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

def test_calibration(file_name, sensor_names):
    with open(file_name) as data_file:
        ts_data = json.load(data_file)

    # pprint(data)
    for ts_hour in ts_data:
        print('start day %s hour %d ' % (ts_hour['day'], int(ts_hour['hour']) - 1,))
        for sensor_vals in ts_hour['data']['timeseries']:
            for sensor_name in sensor_names:
                print('== START %s time=%s' % (sensor_name, sensor_vals['time']))
                sensor_def = SENSOR_DEFS[sensor_name]

                # Step 1 check input(s) validity
                input_name = sensor_def['input']
                input_valid, reason = check_value(input_name, sensor_vals)
                if not input_valid:
                    print('WARN: %s invalid input: input=%s: reason=%s' % (sensor_name, input_name, reason))
                    continue

                print('%s - valid input: input=%s' % (sensor_name, input_name))

                # Step 2 get raw value(s)
                value_raw = get_raw_value(input_name, sensor_vals)
                if value_raw is None:
                    # No use to proceed without raw input value(s)
                    continue

                print('%s - raw input value(s) ok input=%s vals=%s' % (sensor_name, input_name, str(value_raw)))

                # Convert
                value = sensor_def['converter'](value_raw, sensor_vals, sensor_name)
                output_valid, reason = check_value(sensor_name, sensor_vals, value=value)
                if not output_valid:
                    print('WARN: %s invalid output: input=%s: reason=%s' % (sensor_name, input_name, reason))
                    continue

                print('%s - raw output value ok output=%f int_output=%d' % (sensor_name, value, int(round(value))))

                print('== END %s time=%s' % (sensor_name, sensor_vals['time']))


def main():
    """

    """
    test_calibration('data/station-26-raw.json', ['o3', 'no2', 'co'])


if __name__ == "__main__":
    main()
