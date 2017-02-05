import os
import pickle
from stetl.component import Config
from stetl.output import Output
from stetl.packet import FORMAT
from stetl.util import Util

import pandas as pd
import seaborn as sns

from calibration_parameters import param_grid

log = Util.get_log('Visualization')


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
        self.visualization_time_series('20170101', '20170107', 'u1hnvkb')
        self.visualization_time_series('20170101', '20170102', 'u1hnvkb')

    def visualization_error_scatter(self):
        log.info('Visualizing error as scatterplot')
        # Using relative and absolute performance measure
        title = 'Actual vs. Predicted\nRMSE=%.1f ug/m3, Explained ' \
                'var=%.0f%%' % (self.rmse, self.best_score * 100)

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
            self.rmse, self.best_score * 100)

        # Plot using seaborn
        g = sns.distplot(self.sample['error'], 100)
        g.set_title(title)

        self.save_fig('error_histogram')
        self.close_plot()

    def visualization_time_series(self, start_str, end_str, geohash):
        log.info("Visualizing time series %s - %s" % (start_str, end_str))

        start = pd.to_datetime(start_str)
        end = pd.to_datetime(end_str)
        title = 'Timeseries from %s to %s\nRMSE=%.1f ug/m3, Explained ' \
                'var=%.0f%%' % (start, end, self.rmse, self.best_score * 100)

        time_series = self.sample.copy().sort_values('time')
        time_series = time_series[
            (time_series['time'] >= start) & (time_series['time'] <= end) & (
            time_series['geohash'] == geohash)]

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

        self.save_fig('time_series_%s_%s' % (start_str, end_str))
        Visualization.close_plot()


class ModelVisualization(Visualization):
    def __init__(self, configdict, section):
        Visualization.__init__(self, configdict, section)
        self.do_not_consider = None

    def visualization(self):
        self.do_not_consider = ['time', 'geohash', self.target, 'error',
                                'pred']
        # todo use packet.data['sample'] instead
        for col in self.sample.columns.values:
            if col not in self.do_not_consider:
                self.visualization_input_output_relation(col)
        self.save_pickled_model()

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
        ts = sns.tsplot(df, col, 'id', value='Prediction',
                        err_style='unit_traces')

        target_max = self.sample[self.target].max()
        axes = ts.axes
        axes.set_ylim(-50, target_max * 1.1)

        self.save_fig('effect_%s' % col)
        self.close_plot()

    def save_pickled_model(self):
        file_name = 'model.pkl'
        file_path = self.file_path % (self.target, file_name)
        pickle.dump(self.model, open(file_path, 'wb'))
        log.info("Model saved to %s" % file_path)


class DataVisualization(Visualization):
    def visualization(self):
        for col in self.sample.columns.values:
            self.visualization_occurrence(col)

    def visualization_occurrence(self, col):
        log.info('Visualizing occurrence of %s with type %s' % (
        col, self.sample[col].dtype))
        title = 'Occurrence of %s' % col

        if pd.np.issubdtype(self.sample[col].dtype, pd.np.datetime64):
            sns.set_style("darkgrid")
            ax = sns.plt.subplot(111)
            ax.hist(self.sample[col].tolist(), 100, normed=True)
            ax.xaxis_date()
            _, labels = sns.plt.xticks()
            sns.plt.setp(labels, rotation=15)

        elif self.sample[col].dtype == object:
            self.sample[col].groupby(self.sample[col]).count().plot(kind="bar",
                rot=0)

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
