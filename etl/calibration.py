from stetl.component import Config
from stetl.filter import Filter
from stetl.packet import FORMAT
from stetl.util import Util

import pandas as pd
from numpy import nan
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from calibration_parameters import param_grid

log = Util.get_log("Calibration")


class MergeRivmJose(Filter):
    @Config(ptype=dict, required=True)
    def map_jose(self):
        """
        Mapping between Jose stations and "location id's"

        Required: True
        """

    @Config(ptype=dict, required=True)
    def map_rivm(self):
        """
        Mapping between RIVM stations and "location id's"

        Required: True
        """

    def __init__(self, configdict, section, consumes=FORMAT.record_array,
                 produces=FORMAT.record_array):
        Filter.__init__(self, configdict, section, consumes, produces)

    def invoke(self, packet):
        # Convert packet data to dataframes
        result_in = packet.data
        rivm = result_in['rivm']
        jose = result_in['jose']
        df_rivm = pd.DataFrame.from_records(rivm)
        df_jose = pd.DataFrame.from_records(jose)

        log.info("Received rivm data with shape (%d, %d)" % df_rivm.shape)
        log.info("Received jose data with shape (%d, %d)" % df_jose.shape)

        # Rename stations
        df_jose = df_jose.replace({'station': self.map_jose})
        df_rivm = df_rivm.replace({'station': self.map_rivm})

        # Set time as index
        df_rivm['time'] = pd.to_datetime(df_rivm['time'])
        df_jose['time'] = pd.to_datetime(df_jose['time'])

        # Interpolate RIVM to jose times
        jose_index = df_jose['time'].unique()
        jose_time = pd.DataFrame({'time': jose_index})
        df_rivm = jose_time.merge(df_rivm, 'outer').set_index('time')
        df_rivm = df_rivm.sort_index().interpolate().ffill().loc[jose_index]

        # Pivot Jose
        df_jose = df_jose.pivot_table('value', ['station', 'time'],
                                      'component').reset_index()

        # Concatenate RIVM and Jose
        df_rivm = df_rivm.reset_index()
        df_jose = df_jose.reset_index()
        df = pd.merge(df_rivm, df_jose, 'outer', ['time', 'station'])

        log.info("Merged RIVM and Jose data. New shape = (%d, %d)." % df.shape)

        # Select rows and columns
        del df['component']
        del df['index']
        del df['station']
        del df['time']

        df = df.dropna()
        log.info("Dropping NA values. New shape = (%d, %d)." % df.shape)

        packet.data = df.to_dict('records')
        log.info("Returning packet of length %d", len(packet.data))

        return packet


class Calibrator(Filter):
    @Config(ptype=int, default=.01, required=False)
    def inverse_sample_fraction(self):
        """
        Inverse fraction of Jose data to use for calibration. E.g. 10 means
        1/10=0.1.

        Default: 0.01

        Required: True
        """

    @Config(ptype=float, default=.01, required=False)
    def filter_alpha(self):
        """
        Control for low-pass filter, higher alpha is more emphasis on new data

        Default: 0.01

        Required: False
        """

    @Config(ptype=str, required=True)
    def target(self):
        """
        The column to predict, all the other columns will be used for the
        prediction

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

    @Config(ptype=int, default=-2, required=False)
    def n_jobs(self):
        """
        The number of parallel processes to use. Negative values are
        equivalent to total_cores + 1 - njobs

        Default: -2 (all cores - 1)

        Required: False
        """

    def __init__(self, configdict, section, consumes=FORMAT.record_array,
                 produces=FORMAT.record):
        Filter.__init__(self, configdict, section, consumes, produces)
        self.pipeline = None

    def init(self):
        ss = StandardScaler()
        mlp = MLPRegressor(solver='lbfgs')
        steps = [('scale', ss), ('mlp', mlp)]
        self.pipeline = Pipeline(steps)

    def invoke(self, packet):

        log.info("Receiving packet of size %d" % len(packet.data))

        result_out = dict()

        df = pd.DataFrame.from_records(packet.data)
        log.info("Created data frame with shape (%d, %d)" % df.shape)

        # Fitler data
        df = Calibrator.filter_data(df, self.target, self.filter_alpha)

        # Sample to prevent over fitting
        df = df.sample(frac=1 / float(self.inverse_sample_fraction))
        log.info("Sample dataframe, keeping 1 out of every %d rows. New "
                 "shape (%d, %d)" % (
                     self.inverse_sample_fraction, df.shape[0], df.shape[1]))

        # Split into label and data
        x, y = Calibrator.split_data_label(df, self.target)

        log.info("Starting randomized cross validated search to find best "
                 "parameters. Running %d iterations with %d cross "
                 "validations of %d cores" % (
                     self.random_search_iterations, self.cv_k, self.n_jobs))
        gs = RandomizedSearchCV(self.pipeline, param_grid,
                                self.random_search_iterations,
                                n_jobs=self.n_jobs, cv=self.cv_k,
                                error_score=nan)
        gs.fit(x, y)
        log.info("Best result from randomized search: %.2f" % gs.best_score_)
        log.info("Best parameters from randomized search: %s" % str(
            gs.best_params_))

        for gs_keys in ['cv_results_', 'best_estimator_', 'best_score_',
                        'best_params_', 'best_index_', 'scorer_', 'n_splits_']:
            result_out[gs_keys] = getattr(gs, gs_keys)

        packet.data = result_out
        log.info("Returning result of %d length, with keys %s." % (
            len(packet.data), packet.data.keys()))

        return packet

    @staticmethod
    def split_data_label(df, label):
        y = df[label]
        x = df.drop(label, axis=1)
        return x, y

    @staticmethod
    def filter_data(df, target, alpha):
        # todo use rolling mean for time series data
        cols = [df_col for df_col in df.columns if df_col is not target]
        for col in cols:
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
            val = x[0]
        new_x = []
        for (i, elem) in enumerate(x):
            val = elem * alpha + val * (1.0 - alpha)
            new_x.append(val)
        return pd.Series(new_x)
