import sys
from ggplot import *
from matplotlib import pyplot as plt
from numpy import arange, floor, repeat, tile, linspace
from pandas import concat, to_datetime
from pandas import melt

from C import effect_plots, ax_limits, res_limits
from input_output import save_path, load_performances, load_model, load_filter

from input_output import load_predictions


def visualize_scatter(pred, perf, name, limits, path):
    title = '%s\nRMSE=%.1f ug/m3, Explained var=%.0f%%' % \
            (name, perf['rmse'], perf['expl_var']*100)
    p = ggplot(pred, aes(x='target', y='prediction')) + \
        geom_point(alpha=.5) + \
        geom_abline(color='green', size=2) + \
        stat_smooth(method="lm", sd=False, color='blue', size=2) + \
        xlab('Prediction from Jose measurements') + \
        ylab('RIVM measurement') + \
        xlim(limits[0], limits[1]) + \
        ylim(limits[0], limits[1]) + \
        coord_equal() + \
        ggtitle(title)
    p.save(path)


def visualize_residuals(pred, perf, limits, name, path):
    pred['residual'] = pred['target'] - pred['prediction']

    title = '%s\nRMSE=%.2f, Explained var=%.2f%%' % \
            (name, perf['rmse'], perf['expl_var'])
    p = ggplot(pred, aes('residual')) + \
        geom_histogram(bins=500) + \
        xlab('Residual (ug\m3)') + \
        ylab('Count') + \
        xlim(limits[0], limits[1]) + \
        ggtitle(title)
    p.save(path)


def visualize_timeseries(df, start, end, limits, name, path):
    start = to_datetime(start)
    end = to_datetime(end)
    col_num = 'p.unit.serial.number'

    df['secs'] = to_datetime(df['secs'], format='%Y%m%d%H%M%S')
    df = melt(df, [col_num, 'secs'], ['prediction', 'target'], 'Type')
    df = df[(df['secs'] >= start) & (df['secs'] <= end)]
    df[col_num] = df[col_num].astype(int).astype(str)
    df['Location'] = df['Type'].str.cat(df['p.unit.serial.number'])

    p = ggplot(df, aes(x='secs', y='value',  color='Type')) + \
        geom_line(size=2) + \
        ylab('RIVM measurement / Prediction (ug/m3)') + \
        ylim(limits[0], limits[1]) +\
        ggtitle(name)
    if len(df[col_num].unique()) > 1:
        p = p + facet_grid(col_num)
    p.save(path)


def visualize_occurance(pred, col, path):
    p = ggplot(pred, aes(col)) + \
        geom_histogram(bins = 100) + \
        xlab(col) + \
        ylab('Count') + \
        ggtitle('Occurance of %s values' % col)
    p.save(path)


def plot_ann_effect(pipeline, filter, df, col, val, limits, name, path):
    n_times = 100
    n_val = val.shape[0]
    df = df.drop(['prediction', 'target'], axis=1)
    df = filter.transform(df)
    df = df.sample(n_times)
    df = concat([df] * n_val)
    df[col] = repeat(val, n_times)
    df['prediction'] = pipeline.predict(df)
    df['id'] = tile(arange(0, n_times), n_val)

    p = ggplot(df, aes(x=col, y='prediction', group='id')) + \
        geom_line(alpha = .5) + \
        xlab('Jose measurement of %s' % col) + \
        ylab('Prediction for %s' % name) + \
        ylim(limits[0], limits[1]) + \
        ggtitle('Effect of %s on predictions for %s' % (col, name))
    p.save(path)


if __name__ == '__main__':
    col = sys.argv[1]
    t = float(sys.argv[2])

    f_param_optim = save_path('parameter_optimization', col, 'csv', t)
    f_predictions = save_path('predictions', col, 'csv', t)
    f_performance = save_path('performances', col, 'json', t)
    f_model = save_path('model', col, 'pkl', t)
    f_filter = save_path('filter', col, 'pkl', t)

    f_scatter = save_path('scatter', col, 'png', t)
    f_residual = save_path('residual', col, 'png', t)
    f_timeseries = save_path('timeseries', col, 'png', t)

    pred = load_predictions(f_predictions)
    perf = load_performances(f_performance)
    model = load_model(f_model)
    filter = load_filter(f_filter)

    visualize_scatter(pred.copy(), perf, col, ax_limits[col], f_scatter)
    visualize_residuals(pred.copy(), perf, res_limits[col], col, f_residual)
    visualize_timeseries(pred.copy(), "20160515", "20160526", ax_limits[col],
                         col, f_timeseries)

    for name in pred.columns.values:
        f_occurance = save_path('histogram_%s' % name, col, 'png', t)
        visualize_occurance(pred.copy(), name, f_occurance)

    for k, v in effect_plots.iteritems():
        f_effect = save_path('ann_effect_%s' % k, col, 'png', t)
        plot_ann_effect(model, filter, pred.copy(), k, v, ax_limits[col], col,
                        f_effect)
