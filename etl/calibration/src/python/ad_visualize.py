import sys
from ggplot import *
from matplotlib import pyplot as plt
from numpy import arange, floor, repeat, tile, linspace
from pandas import concat

from input_output import save_path, load_performances, load_model, load_filter

from input_output import load_predictions


def visualize_scatter(x, y, perf, path):
    title = 'RMSE=%.2f, Explained var=%.2f%%' % (perf['rmse'],
                                                 perf['expl_var'])
    plt.scatter(x, y)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    plt.xlabel('Predicted')
    plt.ylabel('Measured')
    plt.title(title)
    plt.savefig(path)
    plt.close()


def visualize_residuals(x, y, perf, path):
    title = 'RMSE=%.2f, Explained var=%.2f%%' % (perf['rmse'],
                                                 perf['expl_var'])
    residuals = x - y
    plt.hist(residuals, bins = 100)
    plt.xlabel('Residual')
    plt.ylabel('Count')
    plt.title(title)
    plt.savefig(path)
    plt.close()


def visualize_timeseries(predictions, data):
    # todo
    pass


def plot_ann_effect(pipeline, filter, df, col, val, path):
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
        geom_line(alpha = .5)
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

    pred = load_predictions(f_predictions)
    perf = load_performances(f_performance)
    model = load_model(f_model)
    filter = load_filter(f_filter)

    # visualize_scatter(pred['prediction'], pred['target'], perf, f_scatter)
    # visualize_residuals(pred['prediction'], pred['target'], perf, f_residual)

    n_interp = 100
    effect_plots = {'s.barometer': linspace(970, 1040, n_interp),
                    's.co2': linspace(0, 6500, n_interp),
                    's.humidity': linspace(25, 110, n_interp),
                    's.no2resistance': linspace(0, 2000, n_interp),
                    's.o3resistance': linspace(0, 1500, n_interp),
                    's.temperature.ambient': linspace(-5, 50, 100, n_interp),
                    's.temperature.unit': linspace(0, 60, 100, n_interp)}
    for k, v in effect_plots.iteritems():
        f_effect = save_path('ann_effect_%s' % k, col, 'png', t)
        print(f_effect)
        plot_ann_effect(model, filter, pred, k, v, f_effect)
