"""
Parameter distributions or lists to explore using random/grid search
"""
from scipy.stats import randint, uniform

from distributions import ExpDistribution, FixedLengthTupleDistribution

dist_01 = {'mlp__hidden_layer_sizes': randint(2, 150),
           'mlp__activation': ['logistic', 'tanh', 'relu'],
           'mlp__solver': ['lbgfs'],
           'mlp__alpha': ExpDistribution(uniform(-6, 5)),
           'mlp__learning_rate': ['constant'], 'mlp__max_iter': [200],
           'mlp__learning_rate_init': ExpDistribution(uniform(-6, 5)),
           'filter__alpha': ExpDistribution(uniform(-6, 6))}

layer_size = FixedLengthTupleDistribution([randint(25, 150), randint(2, 50)])
dist_02 = {'mlp__hidden_layer_sizes': layer_size,
           'mlp__activation': ['logistic', 'tanh', 'relu'],
           'mlp__solver': ['sgd'],
           'mlp__alpha': ExpDistribution(uniform(-6, 5)),
           'mlp__batch_size': ['auto'],
           'mlp__learning_rate': ['constant', 'invscaling', 'adaptive'],
           'mlp__max_iter': [10000],
           'mlp__learning_rate_init': ExpDistribution(uniform(-6, 5)),
           'mlp__power_t': uniform(), 'mlp__momentum': uniform(),
           'mlp__nesterovs_momentum': [False, True],
           'mlp__early_stopping': [False, True],
           'filter__alpha': ExpDistribution(uniform(-6, 6))}

CO_final = {'mlp__hidden_layer_sizes': [56],
            'mlp__learning_rate_init': [0.000052997],
            'mlp__alpha': [0.0132466772], 'mlp__momentum': [0.3377605568],
            'mlp__activation': ['relu'], 'mlp__solver': ['lbgfs'],
            'filter__alpha': [0.005]}

O3_final = {'mlp__hidden_layer_sizes': [42],
            'mlp__learning_rate_init': [0.220055322],
            'mlp__alpha': [0.2645091504], 'mlp__momentum': [0.7904790613],
            'mlp__activation': ['logistic'], 'mlp__solver': ['lbgfs'],
            'filter__alpha': [0.005]}

# NO2_final = {'mlp__hidden_layer_sizes': [79], 'mlp__learning_rate_init': [0.0045013008], 'mlp__alpha': [0.1382210543],
#              'mlp__momentum': [0.473310471], 'mlp__activation': ['tanh'], 'mlp__solver': ['lbgfs'],
#              'filter__alpha': [0.005]}
NO2_final = {'mlp__learning_rate': ['constant'],
             'mlp__activation': ['logistic'],
             'filter__alpha': [0.014998264318119752],
             'mlp__alpha': [8.4838007586808904e-06],
             'mlp__learning_rate_init': [0.00023729733377150111],
             'mlp__hidden_layer_sizes': [99], 'mlp__max_iter': [200],
             'mlp__solver': ['lbgfs']}

dist_test = dist_01.copy()
dist_test['mlp__hidden_layer_sizes'] = randint(2, 10)
