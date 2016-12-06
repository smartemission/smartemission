import json
import os
import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_predict


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
