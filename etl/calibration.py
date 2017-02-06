from stetl.component import Config
from stetl.filter import Filter
from stetl.packet import FORMAT
from stetl.util import Util

import matplotlib
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

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


class MergeRivmJose(Filter):
    @Config(ptype=int, default=5, required=True)
    def impute_duration(self):
        """
        Number of minutes to impute data

        Default: 5

        Required: True
        """

    def __init__(self, configdict, section, consumes=FORMAT.record,
                 produces=FORMAT.record):
        Filter.__init__(self, configdict, section, consumes, produces)

    def invoke(self, packet):
        # Convert packet data to dataframes
        result_in = packet.data
        df_rivm = result_in['rivm']
        df_jose = result_in['jose']

        log.info('Received rivm data with shape (%d, %d)' % df_rivm.shape)
        log.info('Received jose data with shape (%d, %d)' % df_jose.shape)
        log.info('Pre-processing geohash and time')

        # Preparing Jose and RIVM data
        df_jose = MergeRivmJose.preproc_geohash_and_time(df_jose)
        df_rivm = MergeRivmJose.preproc_geohash_and_time(df_rivm)
        df_jose = MergeRivmJose.interpolate(df_jose, self.impute_duration * 5)

        # Concatenate RIVM and Jose
        df_index = df_jose.loc[:, ['time', 'geohash']]
        df_rivm = MergeRivmJose.interpolate_to_index(df_index, df_rivm, 60 * 5)
        df = pd.merge(df_jose, df_rivm, 'left', ['time', 'geohash'])
        del df.index.name
        log.info('RIVM and Jose are merged, new shape (%d, %d)' % df.shape)

        # Returning data
        # note: not converting to records, because that take a lot of memory.
        packet.data = {'merged': df}

        return packet

    @staticmethod
    def preproc_geohash_and_time(df):
        df['geohash'] = df['geohash'].str.slice(0, 7)
        df['time'] = pd.to_datetime(df['time'])
        return (df)

    @staticmethod
    def interpolate(df, impute_duration, limit_direction='both'):
        df = df.set_index(['geohash', 'time']).sort_index()
        df = df.interpolate(limit=impute_duration * 5,
                            limit_direction=limit_direction)
        df = df.reset_index()
        return df

    @staticmethod
    def interpolate_to_index(df_index, df_inter, impute_duration):
        log.info('Interpolating RIVM values towards jose measurements')
        df_index['is_index'] = True
        df = df_index.merge(df_inter, 'outer')
        df = MergeRivmJose.interpolate(df, impute_duration)
        df = df[df['is_index'].notnull()]
        df = df.drop('is_index', axis=1)
        return df


class Calibrator(Filter):
    @Config(ptype=int, default=1, required=False)
    def inverse_sample_fraction(self):
        """
        Inverse fraction of Jose data to use for calibration. E.g. 10 means
        1/10=0.1.

        Default: 1

        Required: True
        """

    @Config(ptype=int, default=1, required=False)
    def inverse_filter_alpha(self):
        """
        Control for low-pass filter, higher alpha is more emphasis on new data

        Default: 1

        Required: False
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

    def invoke(self, packet):
        packet.set_end_of_stream(False)

        # Unpacking data
        df = packet.data['merged']
        df = self.drop_rows_and_records(df)
        # df = self.filter_gasses(df)
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
        alpha = 1.0 / float(self.inverse_filter_alpha)
        df = Calibrator.filter_data(df, self._filter, alpha)
        return df

    def optimize_meta_parameters(self, df):
        df = df.drop(['geohash', 'time'], axis=1)

        # Split into label and data
        x, y = Calibrator.split_data_label(df, self.current_target)

        # Order following sensordefs
        input_order = Calibrator.TARGET2SENSORDEF[self.current_target]['input']
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

    @staticmethod
    def filter_data(df, cols, alpha):
        # todo use rolling mean for time series data (i.e. also account for
        # longer gaps in the data)
        if type(cols) is not list:
            cols = [cols]
        for col in cols:
            # log.debug('Filtering %s with alpha=%.3f' % (col, alpha))
            df[col] = Calibrator.running_mean(df[col], alpha)
        return df

    @staticmethod
    def running_mean(x, alpha, start=None):
        """
        Filters a series of observations by a running mean
        new mean = obs * alpha + `previous mean` * (1 - alpha)
        """
        if start is not None:
            val = start
        else:
            val = x.reset_index(drop=True).loc[0]
        new_x = []
        for (i, elem) in enumerate(x):
            val = elem * alpha + val * (1.0 - alpha)
            new_x.append(val)
        return pd.Series(new_x)
