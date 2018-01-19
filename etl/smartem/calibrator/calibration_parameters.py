from scipy.stats import randint, uniform


class ExpDistribution:
    """
    Sample numbers that are exponential of some other distribution
    Note: no normalization takes place, so only use for sampling, not for probabilities
    """

    def __init__(self, original_distribution):
        self.original_distribution = original_distribution

    def rvs(self, random_state=None):
        return pow(10,
                   self.original_distribution.rvs(random_state=random_state))


class VaryingLengthTupleDistribution:
    """
    Sample tuples where each item stems from a source distribution
    Note: this is not a normalized distribution
    """

    def __init__(self, layer_size_distribution, number_of_layers_distribution):
        self.layer_size_distribution = layer_size_distribution
        self.number_of_layers_distribution = number_of_layers_distribution

    def rvs(self, random_state=None):
        num_layers = self.number_of_layers_distribution.rvs(
            random_state=random_state)
        layers = []
        for i in range(num_layers):
            layers.append(
                self.layer_size_distribution.rvs(random_state=random_state))
        return tuple(layers)


class FixedLengthTupleDistribution:
    """
    Tuples where each element stems from a specified distribution
    Note: this is not a normalized distribution
    """

    def __init__(self, distributions):
        self.distributions = distributions

    def rvs(self, random_state=None):
        return tuple([dist.rvs(random_state=random_state) for dist in
                      self.distributions])


param_grid = {'mlp__hidden_layer_sizes': randint(2, 150),
              'mlp__activation': ['logistic', 'tanh', 'relu'],
              'mlp__solver': ['lbfgs'],
              'mlp__alpha': ExpDistribution(uniform(-6, 5)),
              'mlp__learning_rate': ['constant'], 'mlp__max_iter': [200],
              'mlp__learning_rate_init': ExpDistribution(uniform(-6, 5)),
              # no2 results analysis shows good range between 0.1 and 0.001
              # 'filter__alpha': ExpDistribution(uniform(-3, 2)),
              'mlp__early_stopping': [True]}

# CO_best = {'mlp__activation': 'relu', 'mlp__alpha': 1.899210794532138e-06,
#            'mlp__hidden_layer_sizes': 112,
#            'mlp__learning_rate_init': 0.07908998568339845,
#            'mlp__solver': 'lbfgs', 'mlp__learning_rate': 'constant',
#            'mlp__max_iter': 200}
#
# O3_best = {'mlp__activation': 'logistic', 'mlp__alpha': 1.4863204889431821e-05,
#            'mlp__hidden_layer_sizes': 141,
#            'mlp__learning_rate_init': 0.004551945724274247,
#            'mlp__solver': 'lbfgs', 'mlp__learning_rate': 'constant',
#            'mlp__max_iter': 200}
#
# NO2_best = {'mlp__activation': 'tanh', 'mlp__alpha': 1.4312431413452899e-05,
#             'mlp__hidden_layer_sizes': 71,
#             'mlp__learning_rate_init': 4.263969225750196e-05,
#             'mlp__solver': 'lbfgs', 'mlp__learning_rate': 'constant',
#             'mlp__max_iter': 200}
#
# test_grid = param_grid.copy()
# test_grid['mlp__hidden_layer_sizes'] = randint(2, 10)
#
# best_params = {'CO_Waarden': CO_best, 'O3_Waarden': O3_best,
#                'NO2_Waarden': NO2_best}
