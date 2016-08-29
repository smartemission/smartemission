"""
Parameters optimization of artificial neural networks for predict air sensor values
"""
from os import path
from time import mktime, gmtime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig
from sklearn import neural_network as nn
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from data import save_with_pickle, save_with_csv, get_data
from filter import Filter
from measures import rmse
from misc import merge_two_dicts
from params import dist_test, CO_final, O3_final, NO2_final
from results import save_fit_plot

FOLDER_DATA = '/home/pieter/Data/GemeenteNijmegen/SmartEmission/'
FOLDER_SAVE = '/home/pieter/Data/GemeenteNijmegen/SmartEmission/models'
FOLDER_PLOT = '/home/pieter/Documents/GemeenteNijmegen/ANNCalibration/results'


def param_optimization(grid, train_file='train.csv', col_predict='O3_Waarden', cv_k=5, n_part=.1, verbose=1, n_jobs=-1,
                       n_iter=10):
    # Load data
    x_all, y_all, x, y = get_data(FOLDER_DATA, train_file, col_predict, n_part)
    if verbose > 0: print('Using %d data points from now on' % x.shape[0])

    # Create pipeline elements
    mlp = nn.MLPRegressor(activation='logistic', algorithm='l-bfgs', max_iter=5000, early_stopping=True)
    ss = StandardScaler()
    fil = Filter(x_all.to_records(), 1, ('s.co2', 's.no2resistance', 's.o3resistance'), 'secs')
    measure_rmse = make_scorer(rmse, greater_is_better=False)

    # Do randomized grid search
    gs_steps = [('filter', fil), ('scale', ss), ('mlp', mlp)]
    gs_pipe = Pipeline(gs_steps)
    gs = RandomizedSearchCV(gs_pipe, grid, n_iter, measure_rmse, n_jobs=n_jobs, cv=cv_k, verbose=verbose,
                            error_score=np.NaN)
    gs.fit(x, y)

    # Save the results
    save_with_pickle(gs, 'grid_search', FOLDER_SAVE)
    save_with_pickle(gs.best_estimator_, 'best_estimator', FOLDER_SAVE)
    save_with_csv(gs.results_, 'grid_scores', FOLDER_SAVE)

    # Show the results
    print("Best parameters are:\n%s" % gs.best_params_)
    print("Best score is:\n%f" % gs.best_score_)
    save_fit_plot(x, y, gs, FOLDER_PLOT)

    # Filter data
    fil.alpha = gs.best_params_['filter__alpha']
    x = fil.transform(x)
    x = x.drop('secs', axis=1)

    # Learn online estimator
    steps2 = [('scale', ss), ('mlp', mlp)]
    pipe2 = Pipeline(steps2)
    del gs.best_params_['filter__alpha']
    pipe2.set_params(**gs.best_params_)
    pipe2.fit(x, y)

    # Show the results
    save_fit_plot(x, y, pipe2, FOLDER_PLOT)
    save_with_pickle(pipe2, 'actual_estimator', FOLDER_SAVE)


if __name__ == '__main__':
    # param_optimization(dist_test, col_predict='CO_Waarden', n_iter=3, verbose=3, cv_k=3, n_part=0.0001)
    # param_optimization(dist_test, col_predict='O3_Waarden', n_iter=3, verbose=3, cv_k=3, n_part=0.0001)
    # param_optimization(dist_test, col_predict='NO2_Waarden', n_iter=3, verbose=3, cv_k=3, n_part=0.0001)
    param_optimization(CO_final, col_predict='CO_Waarden', n_iter=1, verbose=3, cv_k=10, n_part=0.1)
    param_optimization(O3_final, col_predict='O3_Waarden', n_iter=1, verbose=3, cv_k=10, n_part=0.1)
    param_optimization(NO2_final, col_predict='NO2_Waarden', n_iter=1, verbose=3, cv_k=10, n_part=0.1)
