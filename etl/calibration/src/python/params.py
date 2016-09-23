"""
Parameter distributions or lists to explore using random/grid search
"""
from scipy.stats import randint, uniform

from distributions import ExpDistribution

dist_01 = {'mlp__hidden_layer_sizes': randint(2, 150), 'mlp__learning_rate_init': ExpDistribution(uniform(-12, 11)),
           'mlp__alpha': ExpDistribution(uniform(-12, 11)), 'mlp__momentum': uniform(),
           'mlp__activation': ['logistic', 'tanh', 'relu'], 'mlp__solver': ['l-bfgs'],
           'filter__alpha': ExpDistribution(uniform(-10, 9))}

CO_dist_02 = {'mlp__hidden_layer_sizes': randint(2, 150), 'mlp__learning_rate_init': ExpDistribution(uniform(-12, 12)),
              'mlp__alpha': ExpDistribution(uniform(-12, 12)), 'mlp__momentum': uniform(), 'mlp__activation': ['relu'],
              'mlp__solver': ['l-bfgs'], 'filter__alpha': ExpDistribution(uniform(-12, 12))}

CO_final = {'mlp__hidden_layer_sizes': [56], 'mlp__learning_rate_init': [0.000052997], 'mlp__alpha': [0.0132466772],
            'mlp__momentum': [0.3377605568], 'mlp__activation': ['relu'], 'mlp__solver': ['l-bfgs'],
            'filter__alpha': [0.005]}

O3_final = {'mlp__hidden_layer_sizes': [42], 'mlp__learning_rate_init': [0.220055322], 'mlp__alpha': [0.2645091504],
            'mlp__momentum': [0.7904790613], 'mlp__activation': ['logistic'], 'mlp__solver': ['l-bfgs'],
            'filter__alpha': [0.005]}

NO2_final = {'mlp__hidden_layer_sizes': [79], 'mlp__learning_rate_init': [0.0045013008], 'mlp__alpha': [0.1382210543],
             'mlp__momentum': [0.473310471], 'mlp__activation': ['tanh'], 'mlp__solver': ['l-bfgs'],
             'filter__alpha': [0.005]}

dist_test = {'mlp__hidden_layer_sizes': randint(2, 20), 'mlp__learning_rate_init': ExpDistribution(uniform(-6, 5)),
             'mlp__alpha': ExpDistribution(uniform(-6, 5)), 'mlp__momentum': uniform(), 'mlp__activation': ['logistic'],
             'mlp__solver': ['l-bfgs'], 'filter__alpha': ExpDistribution(uniform(-10, 9))}
