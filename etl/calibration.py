from stetl.component import Config
from stetl.filter import Filter
from stetl.output import Output
from stetl.packet import FORMAT
from stetl.util import Util

import pandas as pd
import os
import matplotlib

matplotlib.use('Agg')
import seaborn as sns
from numpy import nan
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
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
        x, x_test, y, y_test = train_test_split(x, y, test_size=.9)

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
        result_out['out_of_bag'] = (x_test, y_test)
        result_out['target'] = self.target

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


class Visualization(Output):
    @Config(ptype=str, required=True)
    def file_path(self):
        """
        The path where to save the visualization images. Should contain a %s that is replaced by the image name.

        Required: True
        """

    def __init__(self, configdict, section):
        Output.__init__(self, configdict, section, consumes=FORMAT.record)
        self.model = None
        self.oob = None
        self.x = None
        self.y = None
        self.df = None
        self.cv_results_ = None
        self.err = False

    def write(self, packet):
        record_in = packet.data

        self.model = record_in['best_estimator_']

        self.oob = record_in['out_of_bag']
        self.x = self.oob[0]
        self.y = self.oob[1]
        self.df = self.x.copy()
        self.df['Target'] = self.y

        self.cv_results_ = record_in['cv_results_']

        self.target = record_in['target']

        dirname = os.path.dirname(self.file_path)
        log.info("Creating dir %s" % dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.visualize()

        return packet

    def visualize(self):
        pass


class ModelVisualization(Visualization):
    def __init__(self, configdict, section):
        Visualization.__init__(self, configdict, section)
        self.pred = None

    def visualize(self):
        self.pred = self.model.predict(self.x)
        self.df['Prediction'] = self.pred

        self.visualize_error()
        self.visualize_input_output_relation()

    def visualize_error(self):
        # Create title (use both explained variance and rmse to hava a scale
        # relative and absolute measurement of performance)
        expl_var = explained_variance_score(self.y, self.pred)
        rmse = mean_squared_error(self.y, self.pred) ** .5
        title = 'RMSE=%.1f ug/m3, Explained var=%.0f%%' % (
            rmse, expl_var * 100)

        # Plot using seaborn
        g = sns.regplot('Prediction', 'Target', self.df)
        g.set_title(title)
        g.set_aspect('equal', 'datalim')

        # Save
        file_path = self.file_path % 'scatter.png'
        sns.plt.savefig(file_path)
        log.info("Saved scatterplot to %s" % file_path)

    def visualize_input_output_relation(self):
        pass


class SearchVisualization(Visualization):
    def write(self, packet):
        pass

    def visualize(self):
        self.visualize_search()

    def visualize_search(self):
        pass

# def visualize_residuals(pred, perf, limits, name, path):
#     pred['residual'] = pred['target'] - pred['prediction']
#
#     title = '%s\nRMSE=%.2f, Explained var=%.2f%%' % (
#     name, perf['rmse'], perf['expl_var'])
#     p = ggplot(pred, aes('residual')) + geom_histogram(bins=500) + xlab(
#         'Residual (ug\m3)') + ylab('Count') + xlim(limits[0],
#                                                    limits[1]) + ggtitle(
#         title)
#     p.save(path)
#
# def visualize_timeseries(df, start, end, limits, name, path):
#     start = to_datetime(start)
#     end = to_datetime(end)
#     col_num = 'p.unit.serial.number'
#
#     df['secs'] = to_datetime(df['secs'], format='%Y%m%d%H%M%S')
#     df = melt(df, [col_num, 'secs'], ['prediction', 'target'], 'Type')
#     df = df[(df['secs'] >= start) & (df['secs'] <= end)]
#     df[col_num] = df[col_num].astype(int).astype(str)
#     df['Location'] = df['Type'].str.cat(df['p.unit.serial.number'])
#
#     p = ggplot(df, aes(x='secs', y='value', color='Type')) + geom_line(
#         size=2) + ylab('RIVM measurement / Prediction (ug/m3)') + ylim(
#         limits[0], limits[1]) + ggtitle(name)
#     if len(df[col_num].unique()) > 1:
#         p = p + facet_grid(col_num)
#     p.save(path)
#
# def visualize_occurance(pred, col, path):
#     p = ggplot(pred, aes(col)) + geom_histogram(bins=100) + xlab(
#         col) + ylab('Count') + ggtitle('Occurance of %s values' % col)
#     p.save(path)
#
# def plot_ann_effect(pipeline, filter, df, col, val, limits, name, path):
#     n_times = 100
#     n_val = val.shape[0]
#     df = df.drop(['prediction', 'target'], axis=1)
#     df = filter.transform(df)
#     df = df.sample(n_times)
#     df = concat([df] * n_val)
#     df[col] = repeat(val, n_times)
#     df['prediction'] = pipeline.predict(df)
#     df['id'] = tile(arange(0, n_times), n_val)
#
#     p = ggplot(df, aes(x=col, y='prediction', group='id')) + geom_line(
#         alpha=.5) + xlab('Jose measurement of %s' % col) + ylab(
#         'Prediction for %s' % name) + ylim(limits[0], limits[1]) + ggtitle(
#         'Effect of %s on predictions for %s' % (col, name))
#     p.save(path)
#
# if __name__ == '__main__':
#     col = sys.argv[1]
#     t = float(sys.argv[2])
#
#     f_param_optim = save_path('parameter_optimization', col, 'csv', t)
#     f_predictions = save_path('predictions', col, 'csv', t)
#     f_performance = save_path('performances', col, 'json', t)
#     f_model = save_path('model', col, 'pkl', t)
#     f_filter = save_path('filter', col, 'pkl', t)
#
#     f_scatter = save_path('scatter', col, 'png', t)
#     f_residual = save_path('residual', col, 'png', t)
#     f_timeseries = save_path('timeseries', col, 'png', t)
#
#     pred = load_predictions(f_predictions)
#     perf = load_performances(f_performance)
#     model = load_model(f_model)
#     filter = load_filter(f_filter)
#
#     visualize_scatter(pred.copy(), perf, col, ax_limits[col], f_scatter)
#     visualize_residuals(pred.copy(), perf, res_limits[col], col,
#                         f_residual)
#     visualize_timeseries(pred.copy(), "20160515", "20160526",
#                          ax_limits[col], col, f_timeseries)
#
#     for name in pred.columns.values:
#         f_occurance = save_path('histogram_%s' % name, col, 'png', t)
#         visualize_occurance(pred.copy(), name, f_occurance)
#
#     for k, v in effect_plots.iteritems():
#         f_effect = save_path('ann_effect_%s' % k, col, 'png', t)
#         plot_ann_effect(model, filter, pred.copy(), k, v, ax_limits[col],
#                         col, f_effect)
