import json
import os
import pickle
import time

import numpy as np
import pandas as pd
import sys


def save_with_pickle(obj, name, folder):
    f_name = '%012.0f_%s.pkl' % (time.time(), name)
    f_path = os.path.join(folder, f_name)
    with open(f_path, 'wb') as f:
        pickle.dump(obj, f)


def json_save(obj, name, folder):
    f_name = '%012.0f_%s.json' % (time.time(), name)
    f_path = os.path.join(folder, f_name)
    with open(f_path, 'w') as f:
        json.dumps(obj, f)


def save_with_csv(obj, name, folder):
    f_name = '%012.0f_%s.csv' % (time.time(), name)
    f_path = os.path.join(folder, f_name)
    with open(f_path, 'w') as f:
        pd.DataFrame.from_dict(obj).to_csv(f)


def output_save(name, folder):
    f_name = '%012.0f_%s.txt' % (time.time(), name)
    f_path = os.path.join(folder, f_name)
    f = open(f_path, 'w')
    sys.stdout = f
    sys.stderr = f


def get_data(folder, train_file, col_predict, n_part):
    # Load data
    x = pd.read_csv(os.path.join(folder, train_file))

    # Remove outliers for CO
    if col_predict is 'CO_Waarden':
        x = x[np.abs(x.CO_Waarden - x.CO_Waarden.mean()) <= (10 * x.CO_Waarden.std())]

    # Select columns
    cols_predict = ['O3_Waarden', 'NO2_Waarden', 'CO_Waarden']
    x = x.drop([i for i in cols_predict if i is not col_predict], 1)
    x = x.dropna()
    y = x[col_predict].copy()
    x = x.drop(col_predict, 1)

    # Sample data
    n = int(x.shape[0] * n_part)
    idx = np.random.choice(x.shape[0], n)
    sample_x = x.iloc[idx, :].copy()
    sample_y = y.iloc[idx].copy()

    return x, y, sample_x, sample_y
