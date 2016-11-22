import json
import os
import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_predict


def timed_filename(name, extention):
    return '%012.0f_%s.%s' % (time.time(), name, extention)


def save_pickle(obj, name, folder):
    f_name = timed_filename(name, 'pkl')
    f_path = os.path.join(folder, f_name)
    with open(f_path, 'wb') as f:
        pickle.dump(obj, f)


def save_json(obj, name, folder):
    f_name = timed_filename(name, 'json')
    f_path = os.path.join(folder, f_name)
    with open(f_path, 'w') as f:
        json.dumps(obj, f)


def save_csv(obj, name, folder):
    f_name = timed_filename(name, 'csv')
    f_path = os.path.join(folder, f_name)
    with open(f_path, 'w') as f:
        pd.DataFrame.from_dict(obj).to_csv(f)


def save_target_pred(target, pred, name, folder):
    save_csv({'target': target, 'prediction': pred}, name, folder)


def save_txt(obj, name, folder):
    f_name = timed_filename(name, 'txt')
    f_path = os.path.join(folder, f_name)
    with open(f_path, 'w') as f:
        f.write(obj)


def get_csv(folder, train_file, col_predict, n_part):
    # Load data

    # Remove outliers for CO
    if col_predict is 'CO_Waarden':
        x = x[np.abs(x.CO_Waarden - x.CO_Waarden.mean()) <= (
            10 * x.CO_Waarden.std())]

    # Select columns
    cols_predict = ['O3_Waarden', 'NO2_Waarden', 'CO_Waarden']
    x = x.drop([i for i in cols_predict if i != col_predict], 1)
    x = x.dropna()

    y = x[col_predict].copy()
    x = x.drop(col_predict, 1)

    # strata = np.round(x['secs'] / 60 / 60 / 24 / 31) # each 5 days
    # _, sample_x, _, sample_y = train_test_split(x, y, test_size=n_part,
    #                                      stratify = strata)

    n = int(x.shape[0] * n_part)
    idx = np.random.choice(x.shape[0], n)
    sample_x = x.iloc[idx, :].copy()
    sample_y = y.iloc[idx].copy()

    return x, y, sample_x, sample_y


def save_fit_plot(x, y, fit, name, folder):
    predicted = cross_val_predict(fit, x, y, cv=10)
    linfit = np.polyfit(y, predicted, 1)

    fig, ax = plt.subplots()
    ax.scatter(y, predicted, s=1, alpha=.1)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
    ax.plot(y, np.poly1d(linfit)(y), 'g--', lw=2)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    f_name = timed_filename(name, 'pdf')
    plt.savefig(os.path.join(folder, f_name))


def save_parameter_optimization(evaluated_param, path_param_optimization):
    # todo
    pass


def save_predictions(preds, perf, path_predictions):
    # todo
    pass


def save_final_model(final_model, path_final_model):
    # todo
    pass


def save_path(type, gas_component):
    # todo
    pass
