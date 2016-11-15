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

CO_final = {'filter__alpha': [0.0073344041648012058],
            'mlp__alpha': [1.899210794532138e-06], 'mlp__max_iter': [200],
            'mlp__activation': ['relu'], 'mlp__hidden_layer_sizes': [112],
            'mlp__learning_rate': ['constant'], 'mlp__solver': ['lbfgs'],
            'mlp__learning_rate_init': [0.07908998568339845]}

O3_final = {'mlp__activation': ['logistic'],
            'mlp__alpha': [1.4863204889431821e-05],
            'mlp__learning_rate': ['constant'],
            'filter__alpha': [0.0077038310468374709],
            'mlp__learning_rate_init': [0.0045519457242742473],
            'mlp__hidden_layer_sizes': [141], 'mlp__max_iter': [200],
            'mlp__solver': ['lbfgs']}

NO2_final = {'mlp__learning_rate': ['constant'], 'mlp__activation': ['tanh'],
             'mlp__alpha': [1.4312431413452899e-05],
             'mlp__learning_rate_init': [4.2639692257501962e-05],
             'mlp__hidden_layer_sizes': [71], 'mlp__max_iter': [200],
             'mlp__solver': ['lbfgs'], 'filter__alpha': [0.01358001]}
# NO2_final = {'mlp__max_iter': [10000], 'mlp__nesterovs_momentum': [True],
#              'mlp__alpha': [0.001350850267756745],
#              'mlp__early_stopping': [True],
#              'mlp__momentum': [0.41926154492362788],
#              'mlp__hidden_layer_sizes': [(33, 16)], 'mlp__solver': ['sgd'],
#              'mlp__learning_rate': ['adaptive'],
#              'mlp__learning_rate_init': [0.027842603578321252],
#              'filter__alpha': [0.0097972427184488658],
#              'mlp__batch_size': ['auto'], 'mlp__activation': ['tanh']}

dist_test = dist_01.copy()
dist_test['mlp__hidden_layer_sizes'] = randint(2, 10)

final_params = {'CO_Waarden': CO_final, 'O3_Waarden': O3_final,
                'NO2_Waarden': NO2_final}
