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
