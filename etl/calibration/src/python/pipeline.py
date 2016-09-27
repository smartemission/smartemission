"""
Parameters optimization of artificial neural networks for predict air sensor values
"""

import numpy as np
from sklearn import neural_network as nn
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from data import save_pickle, save_csv, get_data, save_fit_plot, save_txt
from filter import Filter
from measures import rmse
from params import dist_01, dist_test, dist_02

FOLDER_DATA = '../../io/data'
FOLDER_SAVE = '../../io/models'
FOLDER_PERF = '../../io/performance'


def param_optimization(grid, col_predict, cv_k=5, n_part=.1,
                       train_file='train.csv', verbose=1, n_jobs=-1, n_iter=10,
                       save=True):
    # Load data
    x_all, y_all, x, y = get_data(FOLDER_DATA, train_file, col_predict, n_part)
    if verbose > 0: print('Using %d data points from now on' % x.shape[0])

    # Create pipeline elements
    mlp = nn.MLPRegressor(activation='logistic', solver='lbgfs', max_iter=5000,
                          early_stopping=True)
    ss = StandardScaler()
    fil = Filter(x_all.to_records(), 1,
                 ('s.co2', 's.no2resistance', 's.o3resistance'), 'secs')
    measure_rmse = make_scorer(rmse, greater_is_better=False)

    # Do randomized grid search
    gs_steps = [('filter', fil), ('scale', ss), ('mlp', mlp)]
    gs_pipe = Pipeline(gs_steps)
    gs = RandomizedSearchCV(gs_pipe, grid, n_iter, measure_rmse, n_jobs=n_jobs,
                            cv=cv_k, verbose=verbose, error_score=np.NaN)
    gs.fit(x, y)
    print("Best parameters are:\n%s" % gs.best_params_)
    print("Best score is:\n%f" % gs.best_score_)

    # Filter data
    fil.alpha = gs.best_params_['filter__alpha']
    x2 = fil.transform(x)
    x2 = x2.drop('secs', axis=1)

    # Learn online estimator
    steps2 = [('scale', ss), ('mlp', mlp)]
    pipe2 = Pipeline(steps2)
    del gs.best_params_['filter__alpha']
    pipe2.set_params(**gs.best_params_)
    pipe2.fit(x2, y)

    if save:
        # Save gridsearch results
        save_pickle(gs, col_predict + '_grid_search', FOLDER_SAVE)
        save_csv(gs.cv_results_, col_predict + '_grid_search_scores',
                 FOLDER_PERF)
        save_txt(str(gs.get_params(True)),
                 col_predict + '_grid_search_parameters', FOLDER_SAVE)

        # Save best estimator
        save_pickle(gs.best_estimator_, col_predict + '_best_estimator',
                    FOLDER_SAVE)
        save_fit_plot(x, y, gs.best_estimator_,
                      col_predict + '_best_estimator_scatter', FOLDER_PERF)
        save_txt(str(gs.best_estimator_.get_params(True)),
                 col_predict + '_best_estimator_parameters', FOLDER_SAVE)

        # Save actual estimator
        save_pickle(pipe2, col_predict + '_actual_estimator', FOLDER_SAVE)
        save_fit_plot(x2, y, pipe2, col_predict + '_actual_estimator_scatter',
                      FOLDER_PERF)
        save_txt(str(pipe2.get_params(True)),
                 col_predict + '_actual_estimator_parameters', FOLDER_SAVE)


if __name__ == '__main__':
    print("Number of models to try:")
    n_iter = input()
    # param_optimization(dist_test, 'CO_Waarden', n_iter=2, verbose=3, cv_k=2,
    #                    n_part=0.0001)
    # param_optimization(dist_test, 'O3_Waarden', n_iter=3, verbose=3, cv_k=3, n_part=0.0001)
    # param_optimization(dist_test, 'NO2_Waarden', n_iter=3, verbose=3, cv_k=3, n_part=0.0001)
    param_optimization(dist_01, 'CO_Waarden', n_iter=n_iter, verbose=3,
                       cv_k=5, n_part=0.02)
    param_optimization(dist_01, 'O3_Waarden', n_iter=n_iter, verbose=3,
                       cv_k=5, n_part=0.02)
    param_optimization(dist_01, 'NO2_Waarden', n_iter=n_iter, verbose=3,
                       cv_k=5, n_part=0.02)
