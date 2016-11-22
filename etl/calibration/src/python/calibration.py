# """
# Parameters optimization of artificial neural networks for predict air sensor values
# """
#
# from math import ceil
#
# import numpy as np
# from sklearn import neural_network as nn
# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.model_selection import cross_val_predict
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler
#
from aa_load_data import *
from ab_prepare_data import *
from ac_model_data import *
from ad_visualize import *
from input_output import save_parameter_optimization, save_final_model, \
    save_predictions, save_path
from params import param_grid, best_params

# from filter import Filter
# from io import save_pickle, save_csv, get_csv, save_fit_plot, save_txt, \
#     save_target_pred
# from params import best_params
#
# FOLDER_DATA = '../../io/data'
# FOLDER_SAVE = '../../io/models'
# FOLDER_PERF = '../../io/performance'


# def param_optimization(grid, col_predict, cv_k=5, n_part=.1,
#                        train_file='train.csv', verbose=1, n_jobs=-1, n_iter=10,
#                        save=True):
#
#     gs = randomized_search(cv_k, grid, pipe, n_iter, n_jobs, verbose, x, y)
#     pipe2, pred2, x2 = learn_online_estimator(cv_k, fil, gs.best_params_, mlp,
#                                               ss, x, y)
#     if save:
#         save_results(col_predict, gs, pipe2, pred2, x, x2, y)
#
#
# def save_results(col_predict, gs, pipe2, pred2, x, x2, y):
#     # Save gridsearch results
#     save_pickle(gs, col_predict + '_grid_search', FOLDER_SAVE)
#     save_csv(gs.cv_results_, col_predict + '_grid_search_scores', FOLDER_PERF)
#     save_txt(str(gs.get_params(True)), col_predict + '_grid_search_parameters',
#              FOLDER_SAVE)
#     # Save best estimator
#     save_pickle(gs.best_estimator_, col_predict + '_best_estimator',
#                 FOLDER_SAVE)
#     save_fit_plot(x, y, gs.best_estimator_,
#                   col_predict + '_best_estimator_scatter', FOLDER_PERF)
#     save_txt(str(gs.best_estimator_.get_params(True)),
#              col_predict + '_best_estimator_parameters', FOLDER_SAVE)
#     # Save actual estimator
#     save_pickle(pipe2, col_predict + '_actual_estimator', FOLDER_SAVE)
#     save_fit_plot(x2, y, pipe2, col_predict + '_actual_estimator_scatter',
#                   FOLDER_PERF)
#     save_txt(str(pipe2.get_params(True)),
#              col_predict + '_actual_estimator_parameters', FOLDER_SAVE)
#     # Save target - prediction pairs
#     save_target_pred(y, pred2, col_predict + '_target_pred', FOLDER_PERF)
#
#
# def learn_online_estimator(cv_k, fil, parameters, mlp, ss, x, y):
#     # Filter data
#     fil.alpha = parameters['filter__alpha']
#     x2 = fil.transform(x)
#     x2 = x2.drop('secs', axis=1)
#     # Learn online estimator
#     steps2 = [('scale', ss), ('mlp', mlp)]
#     pipe2 = Pipeline(steps2)
#     del parameters['filter__alpha']
#     pipe2.set_params(**parameters)
#     pipe2.fit(x2, y)
#     pred2 = cross_val_predict(pipe2, x, y, cv=cv_k)
#     return pipe2, pred2, x2
#
#
# def randomized_search(cv_k, grid, gs_pipe, n_iter, n_jobs, verbose, x, y):
#     gs = RandomizedSearchCV(gs_pipe, grid, n_iter, n_jobs=n_jobs, cv=cv_k,
#                             verbose=verbose, error_score=np.NaN)
#     gs.fit(x, y)
#     print("Best parameters are:\n%s" % gs.best_params_)
#     print("Best score is:\n%f" % gs.best_score_)
#     return gs
#
#

#
#
# def calibrate():
#     print("Specify number of models:")
#     n_iter = int(input())
#     print("Specify number of batches:")
#     n_batches = int(input())
#     print("Specify column to predict (O3_Waarden, NO2_Waarden, CO_Waarden):")
#     col_y = raw_input()
#     col_param = best_params[col_y]
#     n_iter = int(ceil(n_iter / n_batches))
#     for i in range(n_batches):
#         param_optimization(col_param, col_y, n_iter=n_iter, verbose=3, cv_k=9,
#                            n_part=0.02, n_jobs=-1)
#


if __name__ == '__main__':
    path_param_optim = save_path('parameter_optimization', 'O3_Waarden')
    path_predictions = save_path('predictions', 'O3_Waarden')
    path_final_model = save_path('predictions', 'O3_Waarden')

    df_rivm, df_jose = get_rivm_and_jose_data()
    df_rivm = prepare_rivm(df_rivm)
    df_jose = prepare_jose(df_jose)
    df = combine_rivm_and_jose(df_rivm, df_jose, 'O3_Waarden')
    df_cv = get_learn_and_validate_sample(df, 1/100.0)
    x_all, y_all = split_data_label(df, 'O3_Waarden')
    x_cv, y_cv = split_data_label(df_cv, 'O3_Waarden')

    pipe = get_pipeline(df)
    # evaluated_param = optimize_param(pipe, param_grid, data=df)
    # save_parameter_optimization(evaluated_param, path_param_optim)
    #
    # preds, perf = cross_validated_predictions(pipe, best_params['O3_Waarden'])
    # save_predictions(preds, perf, path_predictions)
    #
    # final_model = learn_model(pipe, best_params['O3_Waarden'])
    # final_model = learn_model(pipe, best_params['O3_Waarden'])
    # save_final_model(final_model, path_final_model)
    #
    # visualize_scatter(preds, perf, data=df)
    # visualize_timeseries(preds, data=df)
    # visualize_ann_effect(final_model, data=df)
