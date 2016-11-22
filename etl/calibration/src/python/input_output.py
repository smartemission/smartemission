import json
import os
import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_predict


# def save_pickle(obj, name, folder):
#     f_name = timed_filename(name, 'pkl')
#     f_path = os.path.join(folder, f_name)
#     with open(f_path, 'wb') as f:
#         pickle.dump(obj, f)
#
#
# def save_json(obj, name, folder):
#     f_name = timed_filename(name, 'json')
#     f_path = os.path.join(folder, f_name)
#     with open(f_path, 'w') as f:
#         json.dumps(obj, f)
#
#
# def save_txt(obj, name, folder):
#     f_name = timed_filename(name, 'txt')
#     f_path = os.path.join(folder, f_name)
#     with open(f_path, 'w') as f:
#         f.write(obj)


# def get_csv(folder, train_file, col_predict, n_part):
#     # Load data
#
#     # Remove outliers for CO
#     if col_predict is 'CO_Waarden':
#         x = x[np.abs(x.CO_Waarden - x.CO_Waarden.mean()) <= (
#             10 * x.CO_Waarden.std())]
#
#     # Select columns
#     cols_predict = ['O3_Waarden', 'NO2_Waarden', 'CO_Waarden']
#     x = x.drop([i for i in cols_predict if i != col_predict], 1)
#     x = x.dropna()
#
#     y = x[col_predict].copy()
#     x = x.drop(col_predict, 1)
#
#     # strata = np.round(x['secs'] / 60 / 60 / 24 / 31) # each 5 days
#     # _, sample_x, _, sample_y = train_test_split(x, y, test_size=n_part,
#     #                                      stratify = strata)
#
#     n = int(x.shape[0] * n_part)
#     idx = np.random.choice(x.shape[0], n)
#     sample_x = x.iloc[idx, :].copy()
#     sample_y = y.iloc[idx].copy()
#
#     return x, y, sample_x, sample_y


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


def timed_filename(name, extention, timestamp = None):
    if timestamp is None:
        timestamp = time.time()
    return '%012.0f_%s.%s' % (timestamp, name, extention)


def save_path(type, gas_component, extention, timestamp=None):
    fname = timed_filename(type, extention, timestamp)
    return os.path.join('../../io/results', gas_component, fname)


def save_parameter_optimization(evaluated_param, path):
    with open(path, 'w') as f:
        pd.DataFrame.from_dict(evaluated_param).to_csv(f, index = False)


def load_parameter_optimization(path):
    with open(path, 'r') as f:
        return pd.DataFrame.from_csv(f, index_col = False)


def save_predictions(preds, x, y, path):
    x = x.copy()
    pd.set_option('display.float_format', lambda x: '%05.3f' % x)
    preds = pd.DataFrame({'prediction': preds, 'target': y})
    # x['secs'] = x['secs']
    df = pd.concat([x, preds], axis = 1)
    with open(path, 'w') as f:
        print("WRITING")
        print(path)
        df.to_csv(f, index = False, float_format="%f")


def load_predictions(path):
    with open(path, 'r') as f:
        df = pd.DataFrame.from_csv(f, index_col=False)
        df['secs'] = df['secs'].round().astype(int)
        return df


def save_performances(perf, path):
    with open(path, 'w') as f:
        json.dump(perf, f)


def load_performances(path):
    with open(path, 'r') as f:
        return json.load(f)


def save_model(final_model, path):
    with open(path, 'w') as f:
        pickle.dump(final_model, f)


def load_model(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def save_filter(filter, path):
    with open(path, 'w') as f:
        pickle.dump(filter, f)


def load_filter(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
