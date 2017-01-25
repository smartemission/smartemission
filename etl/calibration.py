import json
import os
from stetl.component import Config
from stetl.filter import Filter
from stetl.inputs.dbinput import PostgresDbInput
from stetl.output import Output
from stetl.outputs.dboutput import PostgresInsertOutput
from stetl.packet import FORMAT
from stetl.util import Util

import matplotlib
import psycopg2
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

matplotlib.use('Agg')
import pandas as pd
import seaborn as sns
import pickle
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

        # Rename stations
        df_jose['geohash'] = df_jose['geohash'].str.slice(0,7)
        df_rivm['geohash'] = df_rivm['geohash'].str.slice(0,7)

        # Set time as index
        df_jose['time'] = pd.to_datetime(df_jose['time'])
        df_rivm['time'] = pd.to_datetime(df_rivm['time'])

        # Interpolate RIVM to jose times
        log.info('Interpolating RIVM values towards jose measurements')
        jose_index = df_jose['time'].unique()
        jose_time = pd.DataFrame({'time': jose_index})
        df_rivm = jose_time.merge(df_rivm, 'outer').set_index('time')
        df_rivm = df_rivm.sort_index().interpolate().ffill().loc[jose_index]
        df_rivm = df_rivm.reset_index()

        # Concatenate RIVM and Jose
        df = pd.merge(df_rivm, df_jose, 'outer', ['time', 'geohash'])
        del df.index.name
        log.info('RIVM and Jose are merged, new shape (%d, %d)' %  df.shape)

        # Filling and dropping na
        log.info('Filling and dropping missing values')
        df = df.sort_values('time')
        df = df.fillna(method='pad', limit=self.impute_duration*5) # 5 min
        log.info("Missing values: %s" % pd.isnull(df).sum().to_dict())
        df = df.dropna()
        log.info('Missing values are removed, new shape (%d, %d).' % df.shape)

        # note: not converting to records, because that take a lot of memory.
        packet.data = {'merged': df}
        log.info('Returning dict with pandas DataFrame as only element')

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

    @Config(ptype=int, default=-2, required=False)
    def n_jobs(self):
        """
        The number of parallel processes to use. Negative values are
        equivalent to total_cores + 1 - njobs

        Default: -2 (all cores - 1)

        Required: False
        """

    def __init__(self, configdict, section, consumes=FORMAT.record,
                 produces=FORMAT.record):
        Filter.__init__(self, configdict, section, consumes, produces)
        self.pipeline = None
        self.current_target = None
        self.current_target_id = None
        self.other_targets = None

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
        log.info('Receiving packet of size %d' % len(packet.data))
        df = packet.data['merged']
        df = df.drop(self.other_targets, axis=1)
        df = df.reset_index().drop('index', axis = 1) # remove possible index
        log.info('Created data frame with shape (%d, %d)' % df.shape)

        # Sample to prevent over fitting
        df = df.sample(frac=1.0 / float(self.inverse_sample_fraction))
        df_meta = df[['geohash', 'time']]
        df = df.drop(['geohash', 'time'], axis=1)
        log.info('Sample data frame, keeping 1 out of every %d rows. New '
                 'shape %s' % (self.inverse_sample_fraction, df.shape))

        # Split into label and data
        x, y = Calibrator.split_data_label(df, self.current_target)
        x = x.reindex_axis(sorted(x.columns), axis=1)

        # Do cross validation
        log.info('Starting randomized cross validated search to find best '
                 'parameters. Running %d iterations with %d cross '
                 'validations of %d cores. Finding relation from %s to %s.' % (
                     self.random_search_iterations, self.cv_k, self.n_jobs,
                     ', '.join(x.columns.tolist()), self.current_target))
        gs = RandomizedSearchCV(self.pipeline, param_grid,
                                self.random_search_iterations,
                                n_jobs=self.n_jobs, cv=self.cv_k,
                                error_score=nan)
        gs.fit(x, y)
        log.info('Best result (%.2f) obtained by using %s' %
                 (gs.best_score_, gs.best_params_))

        # Compute performance and cross val predictions and add meta
        pipe = gs.best_estimator_
        scorer = make_scorer(mean_squared_error, False)
        mses = cross_val_score(pipe, x, y, None, scorer, self.cv_k,
                               n_jobs=self.n_jobs)
        rmse = pd.np.mean(pd.np.sqrt(-mses))

        df = pd.concat([df, df_meta], axis=1)
        df['pred'] = cross_val_predict(pipe, x, y, None, self.cv_k, -1)
        df['error'] = df[self.current_target] - df['pred']

        # Save results
        result_out = dict()
        for gs_keys in ['cv_results_', 'best_estimator_', 'best_score_',
                        'best_params_', 'best_index_', 'scorer_', 'n_splits_']:
            result_out[gs_keys] = getattr(gs, gs_keys)
        result_out['target'] = self.current_target
        # result_out['data'] = df
        result_out['sample'] = df
        result_out['rmse'] = rmse
        result_out['column_order'] = x.columns.tolist()

        packet.data = result_out
        log.info('Returning result of %d length, with keys %s.' % (
            len(packet.data), packet.data.keys()))

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
        cols = [df_col for df_col in df.columns if df_col in cols]
        for col in cols:
            # log.info('Filtering %s with alpha=%.3f' % (col, alpha))
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


class Visualization(Output):
    @Config(ptype=str, required=True)
    def file_path(self):
        """
        The path where to save the visualization images. Should contain a %s that is replaced by the image name.

        Required: True
        """

    @Config(ptype=bool, default=False, required=True)
    def clear_output_folder(self):
        """
        If the results folder should be cleared before putting the new
        results in.

        Default: False

        Required: False
        """

    def __init__(self, configdict, section):
        Output.__init__(self, configdict, section, consumes=FORMAT.record)
        self.model = None
        # self.df = None
        self.sample = None
        self.cv_results_ = None
        self.target = None
        self.best_score = None
        self.rmse = None

    def write(self, packet):
        record_in = packet.data

        self.model = record_in['best_estimator_']
        # self.df = record_in['data']
        self.sample = record_in['sample']
        self.cv_results_ = record_in['cv_results_']
        self.target = record_in['target']
        self.best_score = record_in['best_score_']
        self.rmse = record_in['rmse']

        if self.clear_output_folder:
            folder = os.path.dirname(self.file_path) % self.target
            Visualization.create_empty_folder(folder)
        self.visualization()

        return packet

    def visualization(self):
        pass

    def save_fig(self, file_name, file_extension='png'):
        file_name = "%s.%s" % (file_name, file_extension)
        file_path = self.file_path % (self.target, file_name)
        sns.plt.savefig(file_path)
        log.info('Saved figure to %s' % file_path)

    @staticmethod
    def close_plot():
        sns.plt.close()

    @staticmethod
    def create_empty_folder(folder):
        # Create folder and delete content if exist
        if not os.path.exists(folder):
            log.info('Creating dir %s' % folder)
            os.makedirs(folder)
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                log.info("Error while deleting file: %s" % str(e))


class PerformanceVisualization(Visualization):
    def __init__(self, configdict, section):
        Visualization.__init__(self, configdict, section)

    def visualization(self):
        self.visualization_error_scatter()
        self.visualization_error_histogram()
        self.visualization_time_series('20170101', '20170201', 'u1hnvkb')

    def visualization_error_scatter(self):
        log.info('Visualizing error as scatterplot')
        # Using relative and absolute performance measure
        title = 'Actual vs. Predicted\nRMSE=%.1f ug/m3, Explained ' \
                'var=%.0f%%' % (self.rmse, self.best_score*100)

        g = sns.regplot('pred', self.target, self.sample,
                        scatter_kws={'alpha': 0.3})
        g.set_title(title)
        g.set_aspect('equal', 'box')

        self.save_fig('error_scatter')
        Visualization.close_plot()

    def visualization_error_histogram(self):
        log.info('Visualizing error as histogram')
        # Create title (use both explained variance and rmse to hava a scale
        # relative and absolute measurement of performance)
        title = 'Histogram of error\nRMSE=%.1f ug/m3, Explained var=%.0f%%' % (
            self.rmse, self.best_score*100)

        # Plot using seaborn
        g = sns.distplot(self.sample['error'], 100)
        g.set_title(title)

        self.save_fig('error_histogram')
        self.close_plot()

    def visualization_time_series(self, start, end, geohash):
        log.info("Visualizing time series from %s to %s" % (start, end))

        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        title = 'Timeseries from %s to %s\nRMSE=%.1f ug/m3, Explained ' \
                'var=%.0f%%' % (start, end, self.rmse, self.best_score*100)

        time_series = self.sample.copy().sort_values('time')
        time_series = time_series[(time_series['time'] >= start) &
                                  (time_series['time'] <= end) &
                                  (time_series['geohash'] == geohash)]

        sns.set_style('darkgrid')
        sns.plt.plot(time_series['time'], time_series[self.target])
        sns.plt.plot(time_series['time'], time_series['pred'])
        _, labels = sns.plt.xticks()
        sns.plt.setp(labels, rotation=15)
        sns.plt.xlabel('Time')
        sns.plt.ylabel(self.target)
        sns.plt.title(title)
        sns.plt.legend(['Target', 'Prediction'])
        sns.plt.show()

        self.save_fig('time_series')
        Visualization.close_plot()


class ModelVisualization(Visualization):
    def __init__(self, configdict, section):
        Visualization.__init__(self, configdict, section)
        self.do_not_consider = None

    def visualization(self):
        self.do_not_consider = ['time', 'geohash', self.target, 'error', 'pred']
        # todo use packet.data['sample'] instead
        for col in self.sample.columns.values:
            if col not in self.do_not_consider:
                self.visualization_input_output_relation(col)

    def visualization_input_output_relation(self, col, n_val=100, n_sim=100):
        log.info('Visualizing input/output relation %s' % col)

        df = self.sample.drop(self.do_not_consider, 1)
        val = pd.np.linspace(df[col].min(), df[col].max(), n_val)
        df = df.sample(n_sim)
        df = pd.concat([df] * n_val)
        df[col] = pd.np.repeat(val, n_sim)

        df['Prediction'] = self.model.predict(df)
        df['id'] = pd.np.tile(pd.np.arange(0, n_sim), n_val)

        # index should start at 0 for tsplot.
        # see: https://github.com/mwaskom/seaborn/issues/957
        df = df.reset_index()
        sns.tsplot(df, col, 'id', value='Prediction', err_style='unit_traces')

        self.save_fig('effect_%s' % col)
        self.close_plot()


class DataVisualization(Visualization):
    def visualization(self):
        for col in self.sample.columns.values:
            self.visualization_occurrence(col)

    def visualization_occurrence(self, col):
        log.info('Visualizing occurrence of %s with type %s' % \
                 (col, self.sample[col].dtype))
        title = 'Occurrence of %s' % col

        if pd.np.issubdtype(self.sample[col].dtype, pd.np.datetime64):
            sns.set_style("darkgrid")
            ax = sns.plt.subplot(111)
            ax.hist(self.sample[col].tolist(), 100, normed = True)
            ax.xaxis_date()
            _, labels = sns.plt.xticks()
            sns.plt.setp(labels, rotation=15)

        elif self.sample[col].dtype == object:
            self.sample[col].groupby(self.sample[col]).count().plot(
                kind="bar", rot=0)

        else:
            # use seaborn for other types
            kde = True
            if self.sample[col].unique().shape[0] <= 1:
                kde = False

            g = sns.distplot(self.sample[col], 100, kde=kde)
            g.set_title(title)

        self.save_fig('histogram_%s' % col)
        Visualization.close_plot()


class SearchVisualization(Visualization):
    def __init__(self, configdict, section):
        Visualization.__init__(self, configdict, section)
        self.cv_results = None

    def visualization(self):
        self.visualization_init()
        for col in param_grid.keys():
            self.visualize_search_parameter(col)

    def visualization_init(self):
        self.cv_results = pd.DataFrame(self.cv_results_)

    def visualize_search_parameter(self, param):
        log.info('Visualizing parameter performance of %s' % param)

        title = "Explained variances for different levels of %s" % param
        col = "param_%s" % param
        col_score = "mean_test_score"
        col_type = type(self.cv_results[col][0])

        if col_type is str or col_type is bool:
            g = sns.swarmplot(col, col_score, data=self.cv_results)
        else:
            g = self.cv_results.plot(col, col_score, 'scatter')

        g.set(ylim=(0, 1))
        g.set_title(title)

        self.save_fig('parameter_%s' % param)
        self.close_plot()


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


class CalibrationModelInput(PostgresDbInput):
    """
    Get unpickled calibration model from the database
    """

    @Config(ptype=dict, default=dict(), required=False)
    def sensor_model_names(self):
        """
        The name of the sensor models in the database. Needed for linking
        the right model to the right gas.

        Default: dict()

        Required: False
        """

    def __init__(self, configdict, section):
        PostgresDbInput.__init__(self, configdict, section)
        self.models = None

    def init(self):
        PostgresDbInput.init(self)

        def get_model(name):
            query = self.query % name
            log.info('Getting calibration model with query: %s' % query)
            ret = self.raw_query(query)
            if len(ret) > 0:
                return pickle.loads(str(ret[0][0]))
            else:
                log.warn("No model found for %s" % name)
                return None

        if self.query is not None and len(
                self.sensor_model_names) > 0:
            log.info('Getting calibration models from database')
            self.models = {k: get_model(v) for k, v in
                           self.sensor_model_names.iteritems()}
        else:
            log.info(
                'No query for fetching calibration models given or no '
                'mapping for calibration models to gas components given.')

    def invoke(self, packet):
        packet.meta['models'] = self.models

        return packet


