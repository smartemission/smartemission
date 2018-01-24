from stetl.component import Config
from stetl.filter import Filter
from stetl.packet import FORMAT
from stetl.util import Util

import matplotlib
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

from smartem.util.running_mean import RunningMean
from smartem.devices.josene import Josene

matplotlib.use('Agg')
import pandas as pd
from numpy import nan
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from calibration_parameters import param_grid

log = Util.get_log('Calibration')


class Calibrator(Filter):
    """
    Builds the ANN Calibration model.
    """

    @Config(ptype=int, default=1, required=False)
    def inverse_sample_fraction(self):
        """
        Inverse fraction of Jose data to use for calibration. E.g. 10 means
        1/10=0.1.

        Default: 1

        Required: True
        """

    @Config(ptype=dict, default={}, required=True)
    def running_means(self):
        """
        Columns to apply running mean on and with what weight.

        Example: {'s_coresistance': 0.05,
                  's_oresistance': 0.05,
                  's_no2resistance':  0.05}

        Default: {}
        Required: True
        """

    @Config(ptype=list, required=True)
    def targets(self):
        """
        The columns to predict. For each prediction all the columns that are
        not in this list will be used for prediction.

        Required: True
        """

    @Config(ptype=int, default=100, required=False)
    def random_search_iterations(self):
        """
        The number of random parameter settings to try before choosing the
        best one.

        Default: 100

        Required: False
        """

    @Config(ptype=int, default=10, required=False)
    def cv_k(self):
        """
        The number of cross-validations to perform

        Default: 10

        Required: False
        """

    @Config(ptype=int, default=1, required=False)
    def n_jobs(self):
        """
        The number of parallel processes to use. Negative values are
        equivalent to total_cores + 1 - njobs

        Default: 1

        Required: False
        """

    TARGET2SENSORDEF = {'carbon_monoxide__air_': 'co',
                           'nitrogen_dioxide__air_': 'no2',
                           'ozone__air_': 'o3'}

    def __init__(self, configdict, section, consumes=FORMAT.record,
                 produces=FORMAT.record):
        Filter.__init__(self, configdict, section, consumes, produces)
        self.pipeline = None
        self.current_target = None
        self.current_target_id = None
        self.other_targets = None
        self._filter = ['s_coresistance', 's_no2resistance', 's_o3resistance']
        self._return_gs_elem = ['cv_results_', 'best_estimator_',
                                'best_score_', 'best_params_', 'best_index_',
                                'scorer_', 'n_splits_']
        self.sensor_defs = Josene().get_sensor_defs()

    def init(self):
        ss = StandardScaler()
        mlp = MLPRegressor(solver='lbfgs')
        steps = [('scale', ss), ('mlp', mlp)]
        self.pipeline = Pipeline(steps)
        self.current_target_id = -1
        if self.has_next_target():
            self.next_target()

    def next_target(self):
        self.current_target_id += 1
        self.current_target = self.targets[self.current_target_id]
        self.other_targets = self.targets[:]
        self.other_targets.remove(self.current_target)

    def has_next_target(self):
        return self.current_target_id + 1 < len(self.targets)

    def current_sensordef(self):
        return self.sensor_defs[Calibrator.TARGET2SENSORDEF[self.current_target]]

    def invoke(self, packet):
        packet.set_end_of_stream(False)

        # Unpacking data
        df = packet.data['merged']
        df = self.drop_rows_and_records(df)
        df = self.filter_gasses(df)
        df = df.sample(frac=1.0 / float(self.inverse_sample_fraction))
        log.info('After dropping, filtering and sampling a data frame with '
                 'shape (%d, %d) is ready for calibration' % df.shape)

        # optimize
        gs, x, y = self.optimize_meta_parameters(df)
        best_estimator = gs.best_estimator_

        # Cross validated performance and prediction
        rmse = self.compute_cv_performance(best_estimator, x, y)
        df = self.compute_cv_error(best_estimator, df, x, y)

        # Save results
        result_out = dict()
        for gs_keys in self._return_gs_elem:
            result_out[gs_keys] = getattr(gs, gs_keys)
        result_out['running_means'] = self.running_means
        result_out['target'] = self.current_target
        result_out['sample'] = df
        result_out['rmse'] = rmse
        result_out['column_order'] = x.columns.tolist()

        # Return results
        packet.data = result_out
        packet = self.stop_at_end_of_stream(packet)
        log.info('Returning packet of size %d' % len(packet.data))

        return packet

    def drop_rows_and_records(self, df):
        df = df.drop(self.other_targets, axis=1)
        df = df.dropna()
        df = df.reset_index(drop=True)
        return df

    def filter_gasses(self, df):
        df = df.sort_values('time')
        for component in self.running_means:
            f = lambda x: RunningMean.series_running_mean(x, self.running_means[component])
            df[component] = df.groupby('geohash')[component].transform(f)

        return df

    def optimize_meta_parameters(self, df):
        df = df.drop(['geohash', 'time'], axis=1)

        # Split into label and data
        x, y = Calibrator.split_data_label(df, self.current_target)

        # Order following sensordefs
        input_order = self.current_sensordef()['input']
        x = x[input_order]

        # Do cross validation
        log.info('Starting randomized cross validated search to find best '
                 'parameters. Running %d iterations with %d cross validations '
                 'of %d cores. Finding relation from %s to %s.' % (
                     self.random_search_iterations, self.cv_k, self.n_jobs,
                     ', '.join(x.columns.tolist()), self.current_target))
        gs = RandomizedSearchCV(self.pipeline, param_grid,
                                self.random_search_iterations,
                                n_jobs=self.n_jobs, cv=self.cv_k,
                                error_score=nan)
        gs.fit(x, y)
        log.info('Best result (%.2f) obtained by using %s' % (
            gs.best_score_, gs.best_params_))

        return gs, x, y

    def compute_cv_performance(self, best_estimator, x, y):
        scorer = make_scorer(mean_squared_error, False)
        mses = cross_val_score(best_estimator, x, y, None, scorer, self.cv_k,
                               n_jobs=self.n_jobs)
        rmse = pd.np.mean(pd.np.sqrt(-mses))
        return rmse

    def compute_cv_error(self, fit, df, x, y):
        df['pred'] = cross_val_predict(fit, x, y, None, self.cv_k, -1)
        df['error'] = df[self.current_target] - df['pred']
        return df

    def stop_at_end_of_stream(self, packet):
        # Stop calibrating if not targets are left
        if self.has_next_target():
            self.next_target()
        else:
            packet.set_end_of_stream()
        return packet

    @staticmethod
    def split_data_label(df, label):
        y = df[label]
        x = df.drop(label, axis=1)
        return x, y
