import numpy as np
from matplotlib import pyplot as plt

from calibration import load_data, pipeline_elements, learn_online_estimator, \
    randomized_search
from params import best_params


def param_optimization(grid, col_predict, cv_k=5, n_part=.1,
                       train_file='train.csv', verbose=1):
    x, x_all, y, y_all = load_data(col_predict, n_part, train_file, verbose)
    fil, pipe, mlp, ss = pipeline_elements(x_all)

    idx_train, idx_test = train_test_time(x_all, x)
    x_train = x[idx_train]
    y_train = y[idx_train]
    x_test = x_all[idx_test]
    y_test = y_all[idx_test]

    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

    gs = randomized_search(cv_k, grid, pipe, 1, -1, verbose, x_train, y_train)
    pipe2, pred2, x2 = learn_online_estimator(cv_k, fil, gs.best_params_, mlp,
                                              ss, x_train, y_train)

    idx = np.arange(0, x_test.shape[0], 10)
    x_test1 = x_test.iloc[idx]
    y_test1 = y_test.iloc[idx]
    x_secs1 = x_test1['secs']
    x_test1 = x_test1.drop('secs', axis=1)
    p_test1 = pipe2.predict(x_test1)

    plt.plot(x_secs1, y_test1)
    plt.plot(x_secs1, p_test1)
    plt.legend(['Actual', 'Predicted'])
    plt.savefig('scatter1.pdf')

    plt.cla()
    idx = np.arange(0, 10000, 3 * 60)
    x_test2 = x_all.iloc[idx]
    y_test2 = y_all.iloc[idx]
    x_test2 = x_test2.drop('secs', axis=1)
    p_test2 = pipe2.predict(x_test2)

    plt.plot(np.arange(0, y_test2.shape[0]), y_test2)
    plt.plot(np.arange(0, y_test2.shape[0]), p_test2)
    plt.legend(['Actual', 'Predicted'])
    plt.savefig('scatter2.pdf')


def train_test_time(x_all, x):
    idx_low = x.secs < 1e10
    x['secs'] = np.where(idx_low, x['secs'], x['secs'] - 1e10)
    secs_cutoff = np.percentile(x.secs, 90)
    idx_train = x.secs < secs_cutoff
    # x['secs'] = np.where(idx_low, x['secs'], x['secs'] + 1e10)

    idx_low = x_all.secs < 1e10
    x_all['secs'] = np.where(idx_low, x_all['secs'], x_all['secs'] - 1e10)
    idx_test = x_all.secs >= secs_cutoff
    # x_all['secs'] = np.where(idx_low, x_all['secs'], x_all['secs'] + 1e10)

    return idx_train, idx_test


if __name__ == '__main__':
    print("Specify column to predict (O3_Waarden, NO2_Waarden, CO_Waarden):")
    # col_y = raw_input()
    col_y = "O3_Waarden"
    col_param = best_params[col_y]
    param_optimization(col_param, col_y, verbose=3, cv_k=2, n_part=0.05)
