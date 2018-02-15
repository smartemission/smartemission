# -*- coding: utf-8 -*-
#
# Josene ('jose') Device implementation.
#
# Author: Just van den Broecke - 2018

import json
import logging
import pickle
from device import Device
from stetl.postgis import PostGIS
from josenedefs import SENSOR_DEFS
from smartem.util.running_mean import RunningMean

log = logging.getLogger('JoseneDevice')


class Josene(Device):

    def __init__(self):
        Device.__init__(self, 'jose')
        self.model_query = "SELECT id,parameters,model from calibration_models WHERE predicts = '%s' AND invalid = FALSE ORDER BY timestamp DESC LIMIT 1"
        self.state_query = "SELECT state from calibration_state WHERE process = '%s' AND model_id = %d ORDER BY timestamp DESC LIMIT 1"
        self.state_insert = "INSERT INTO calibration_state (process, model_id, state) VALUES ('%s', %d, '%s')"
        self.sensor_model_names = {
            'co': 'carbon_monoxide__air_',
            'no2': 'nitrogen_dioxide__air_',
            'o3': 'ozone__air_'
        }
        self.config_dict = None

    def init(self, config_dict):

        self.config_dict = config_dict
        self.process_name = config_dict['process_name']
        self.db = PostGIS(config_dict)
        self.db.connect()

        ids = dict()
        parameters = dict()
        models = dict()
        state = dict()

        # Query ANN Calibration Model and its State from DB for each calibrated sensor.
        if self.model_query is not None and len(self.sensor_model_names) > 0:
            log.info('Getting calibration models and state from database')
            for k in self.sensor_model_names:
                v = self.sensor_model_names[k]
                id, param, model = self.query_model(v)
                ids[k] = id
                parameters[k] = param
                models[k] = model

                model_state = self.query_state(id)
                state[k] = model_state

        else:
            log.info('No query for fetching calibration models given or no '
                     'mapping for calibration models to gas components given.')

        # Put Model and State info in the Device definitions.
        for k in ids:
            SENSOR_DEFS[k]['converter_model']['model_id'] = ids[k]
        for k in parameters:
            SENSOR_DEFS[k]['converter_model']['running_mean_weights'] = parameters[k]
        for k in models:
            SENSOR_DEFS[k]['converter_model']['mlp_regressor'] = models[k]
        for k, v in state.iteritems():
            for device_id, device_state in v.iteritems():
                for gas, state in device_state.iteritems():
                    v[device_id][gas] = RunningMean.from_dict(state)
            SENSOR_DEFS[k]['converter_model']['state'] = v

    def exit(self):
        # Save the calibration state.
        for k in self.sensor_model_names:
            model = SENSOR_DEFS[k]['converter_model']
            self.save_state(model['model_id'], json.dumps(model['state']))

        self.db.commit(close=False)

    def get_sensor_defs(self):
        return SENSOR_DEFS

    def raw_query(self, query_str):
        self.db.execute(query_str)

        db_records = self.db.cursor.fetchall()
        log.info('read recs: %d' % len(db_records))

        return db_records

    def query_model(self, name):
        query = self.model_query % name
        log.info('Getting calibration model with query: %s' % query)
        ret = self.raw_query(query)
        if len(ret) > 0:
            id, parameters, model = ret[0]
            return id, parameters, pickle.loads(model)
        else:
            log.warn("No model found for %s" % name)
            return None, {}, {}

    def query_state(self, model_id):
        query = self.state_query % (self.process_name, model_id)
        log.info('Getting calibration model state with query: %s' % query)
        ret = self.raw_query(query)
        if len(ret) > 0:
            return ret[0][0]
        else:
            log.warn("No state found for model_id=%d" % model_id)
            return {}

    def save_state(self, model_id, state):
        insert_query = self.state_insert % (self.process_name, model_id, state)
        log.info('Inserting calibration model state for process %s model_id=%d' % (self.process_name, model_id))

        ret = self.db.execute(insert_query)
        if ret != 1:
            log.warn('Cannot save state for process %s model_id=%d' % (self.process_name, model_id))

    # Get raw sensor value or list of values
    def get_raw_value(self, name, val_dict):
        val = None
        if type(name) is list:
            name = name[0]
            return self.get_raw_value(name, val_dict)
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

        if 'audio' in name:
            # We may have audio encoded in 3 bands
            bands = [float(val & 255), float((val >> 8) & 255), float((val >> 16) & 255)]
            val = bands[0]

        return val, name

    # Check for valid sensor value
    def check_value(self, name, val_dict, value=None):
        val = None
        if type(name) is list:
            # name is list of names
            for n in name:
                result, reason = self.check_value(n, val_dict, value)
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

                # Audio inputs: need to unpack 3 bands and check for decibel vals
                if 'audio' in name:
                    bands = [float(val & 255), float((val >> 8) & 255), float((val >> 16) & 255)]

                    # determine validity of these 3 bands
                    dbMin = name_def['min']
                    dbMax = name_def['max']
                    err_cnt = 0
                    msg = ''
                    for i in range(0, len(bands)):
                        band_val = bands[i]
                        # accumulate outliers
                        if band_val < dbMin:
                            err_cnt +=1
                            msg += '%s: val(%s) < min(%s)\n' % (name, str(band_val), str(name_def['min']))
                        elif band_val > dbMax:
                            err_cnt +=1
                            msg += '%s: val(%s) > max(%s)\n' % (name, str(band_val), str(name_def['max']))

                    # Only invalid if all bands outside range
                    if err_cnt >= len(bands):
                        return False, msg

                    return True, '%s OK' % name

                if 'min' in name_def and val < name_def['min']:
                    return False, '%s: val(%s) < min(%s)' % (name, str(val), str(name_def['min']))

                if 'max' in name_def and val > name_def['max']:
                    return False, '%s: val(%s) > max(%s)' % (name, str(val), str(name_def['max']))

        return True, '%s OK' % name

    # Get location as lon, lat
    def get_lon_lat(self, val_dict):
        result = (None, None)
        if 's_longitude' in val_dict and 's_latitude' in val_dict:
            lon = SENSOR_DEFS['longitude']['converter'](val_dict['s_longitude'])
            lat = SENSOR_DEFS['latitude']['converter'](val_dict['s_latitude'])

            valid, reason = self.check_value('latitude', val_dict, value=lat)
            if not valid:
                return result

            valid, reason = self.check_value('longitude', val_dict, value=lon)
            if not valid:
                return result

            result = (lon, lat)

        return result
