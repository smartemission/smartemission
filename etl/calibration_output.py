import json
import pickle
import random
import sys

from stetl.component import Config
from stetl.outputs.dboutput import PostgresInsertOutput
from stetl.outputs.fileoutput import FileOutput
from stetl.util import Util

import pandas as pd
import psycopg2

from sensordefs import SENSOR_DEFS

log = Util.get_log('Calibration output')


class CalibrationDataOutput(FileOutput):
    """
    Saves the calibration data to a file. Assumes that the packet is a dict
    with a pandas DataFrame under the "merged" key.
    """

    def write(self, packet):
        df = packet.data['merged']

        file_path = self.cfg.get('file_path')
        df.to_csv(file_path)

        return packet


class CalibrationModelOutput(PostgresInsertOutput):

    def before_invoke(self, packet):
        result_in = packet.data

        result_out = dict()
        dump = pickle.dumps(result_in['best_estimator_'])
        result_out['model'] = psycopg2.Binary(dump)
        result_out['predicts'] = result_in['target']
        result_out['score'] = result_in['best_score_']
        result_out['n'] = result_in['sample'].shape[0]
        result_out['input_order'] = json.dumps(result_in['column_order'])

        packet.data = result_out

        return packet


class ParameterOutput(PostgresInsertOutput):

    def before_invoke(self, packet):
        result_in = packet.data
        df = pd.DataFrame(result_in['cv_results_'])

        # add id's to keep track of which parameters belong together
        df['search_id'] = random.randint(-sys.maxint, sys.maxint)
        df['setting_id'] = range(df.shape[0])

        param_col = [col for col in list(df) if col.startswith('param_')]
        fixed_col = ['mean_test_score', 'std_test_score', 'rank_test_score',
                    'mean_train_score', 'std_train_score', 'mean_fit_time',
                    'std_fit_time', 'search_id', 'setting_id']
        df = df.loc[:, param_col + fixed_col]
        df = pd.melt(df, fixed_col, param_col, 'parameter', 'value')
        df['value'] = df['value'].astype(str)
        df['n'] = result_in['sample'].shape[0]
        df['predicts'] = result_in['target']

        result_out = df.to_dict('records')
        packet.data = result_out

        return packet


class CalibrationStateOutput(PostgresInsertOutput):

    @Config(ptype=dict, default=dict(), required=False)
    def sensor_model_names(self):
        """
        The name of the sensor models in the database. Needed for linking
        the right model to the right gas.

        Default: dict()

        Required: False
        """

    @Config(ptype=str, required=True)
    def process_name(self):
        """
        The name of the process in which this calibration model is used. The
        name is used to get the right state of the model.

        Required: True
        """

    def before_invoke(self, packet):
        result_out = list()

        if packet.is_end_of_stream():
            for k, v in self.sensor_model_names.iteritems():
                model = SENSOR_DEFS[k]['converter_model']
                result_out.append({'process': self.process_name,
                                   'model_id': model['model_id'],
                                   'state': json.dumps(model['state'])})

        packet.data = result_out

        return packet



