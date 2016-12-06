"""
Parameters optimization of artificial neural networks for predict air sensor values
"""

from load_data import *
from prepare_data import *
from model_data import *
from visualize import *
from input_output import save_parameter_optimization, save_model, \
    save_predictions, save_path, save_performances, save_filter
from pipe_params import param_grid, best_params


if __name__ == '__main__':
    col = sys.argv[2]
    train_path = sys.argv[1]
    
    path_param_optim = save_path('parameter_optimization', col, 'csv')
    path_predictions = save_path('predictions', col, 'csv')
    path_performance = save_path('performances', col, 'json')
    path_model = save_path('model', col, 'pkl')
    path_filter = save_path('filter', col, 'pkl')

    df_rivm, df_jose = get_rivm_and_jose_data(train_path)
    df_rivm = prepare_rivm(df_rivm)
    df_jose = prepare_jose(df_jose)
    df = combine_rivm_and_jose(df_rivm, df_jose, col)
    df_cv = get_learn_and_validate_sample(df, C.sample_ratio)
    x_all, y_all = split_data_label(df, col)
    x_cv, y_cv = split_data_label(df_cv, col)

    pipe = get_pipeline(df)

    evaluated_param = optimize_param(pipe, param_grid, x=x_cv, y=y_cv)
    save_parameter_optimization(evaluated_param, path_param_optim)

    preds, perfs = cv_predictions(pipe, best_params[col], x_cv, y_cv)
    save_predictions(preds, x_cv, y_cv, path_predictions)
    save_performances(perfs, path_performance)

    model, filter = learn_final_model(pipe, best_params[col], x_cv,
                                      y_cv)
    save_model(model, path_model)
    save_filter(filter, path_filter)
