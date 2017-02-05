import json
import pickle
from stetl.outputs.dboutput import PostgresInsertOutput
from stetl.outputs.fileoutput import FileOutput
from stetl.util import Util

import pandas as pd
import psycopg2

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

        param_col = [col for col in list(df) if col.startswith('param_')]
        fixed_col = ['mean_test_score', 'std_test_score', 'rank_test_score',
                    'mean_train_score', 'std_train_score', 'mean_fit_time',
                    'std_fit_time']
        df = df.loc[:, param_col + fixed_col]
        df = pd.melt(df, fixed_col, param_col, 'parameter', 'value')
        df['value'] = df['value'].astype(str)
        df['n'] = result_in['sample'].shape[0]
        df['predicts'] = result_in['target']

        result_out = df.to_dict('records')
        packet.data = result_out

        return packet

