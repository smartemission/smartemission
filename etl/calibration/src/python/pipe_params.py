"""
Parameter distributions or lists to explore using random/grid search
"""
from scipy.stats import randint, uniform

from pipe_distributions import ExpDistribution

param_grid = {'mlp__hidden_layer_sizes': randint(2, 150),
              'mlp__activation': ['logistic', 'tanh', 'relu'],
              'mlp__solver': ['lbfgs'],
              'mlp__alpha': ExpDistribution(uniform(-6, 5)),
              'mlp__learning_rate': ['constant'], 'mlp__max_iter': [200],
              'mlp__learning_rate_init': ExpDistribution(uniform(-6, 5)),
              # no2 results analysis shows good range between 0.1 and 0.001
              'filter__alpha': ExpDistribution(uniform(-3, 2)),
              'mlp__early_stopping': [True]}

# layer_size = FixedLengthTupleDistribution([randint(25, 150), randint(2, 50)])
# dist_02 = {'mlp__hidden_layer_sizes': layer_size,
#            'mlp__activation': ['logistic', 'tanh', 'relu'],
#            'mlp__solver': ['sgd'],
#            'mlp__alpha': ExpDistribution(uniform(-6, 5)),
#            'mlp__batch_size': ['auto'],
#            'mlp__learning_rate': ['constant', 'invscaling', 'adaptive'],
#            'mlp__max_iter': [10000],
#            'mlp__learning_rate_init': ExpDistribution(uniform(-6, 5)),
#            'mlp__power_t': uniform(), 'mlp__momentum': uniform(),
#            'mlp__nesterovs_momentum': [False, True],
#            'mlp__early_stopping': [False, True],
#            'filter__alpha': ExpDistribution(uniform(-6, 6))}

CO_best = {'mlp__activation': 'relu', 'mlp__alpha': 1.899210794532138e-06,
           'mlp__hidden_layer_sizes': 112,
           'mlp__learning_rate_init': 0.07908998568339845,
           'mlp__solver': 'lbfgs', 'mlp__learning_rate': 'constant',
           'mlp__max_iter': 200}

O3_best = {'mlp__activation': 'logistic', 'mlp__alpha': 1.4863204889431821e-05,
           'mlp__hidden_layer_sizes': 141,
           'mlp__learning_rate_init': 0.004551945724274247,
           'mlp__solver': 'lbfgs', 'mlp__learning_rate': 'constant',
           'mlp__max_iter': 200}

NO2_best = {'mlp__activation': 'tanh', 'mlp__alpha': 1.4312431413452899e-05,
            'mlp__hidden_layer_sizes': 71,
            'mlp__learning_rate_init': 4.263969225750196e-05,
            'mlp__solver': 'lbfgs', 'mlp__learning_rate': 'constant',
            'mlp__max_iter': 200}

test_grid = param_grid.copy()
test_grid['mlp__hidden_layer_sizes'] = randint(2, 10)

best_params = {'CO_Waarden': CO_best, 'O3_Waarden': O3_best,
               'NO2_Waarden': NO2_best}
