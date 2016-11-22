from os import path
from time import mktime, gmtime

from matplotlib import pyplot as plt

from input_output import save_path, load_performances

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


def visualize_ann_effect(pipeline, data):
    # todo
    pass


if __name__ == '__main__':
    t = 1479826709
    f_param_optim = save_path('parameter_optimization', 'O3_Waarden', 'csv', t)
    f_predictions = save_path('predictions', 'O3_Waarden', 'csv', t)
    f_performance = save_path('performances', 'O3_Waarden', 'json', t)
    f_final_model = save_path('predictions', 'O3_Waarden', 'pkl', t)

    f_scatter = save_path('scatter', 'O3_Waarden', 'png', t)
    f_residual = save_path('residual', 'O3_Waarden', 'png', t)

    pred = load_predictions(f_predictions)
    perf = load_performances(f_performance)

    visualize_scatter(pred['prediction'], pred['target'], perf, f_scatter)
    visualize_residuals(pred['prediction'], pred['target'], perf, f_residual)
