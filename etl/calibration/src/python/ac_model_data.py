from sklearn import neural_network as nn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from pipeline_elements import Filter


def get_pipeline(data):
    fil = Filter(data, 1, ['s.co2', 's.no2resistance', 's.o3resistance'],
                 ['secs', 'p.unit.serial.number'])
    ss = StandardScaler()
    mlp = nn.MLPRegressor()
    steps = [('filter', fil), ('scale', ss), ('mlp', mlp)]
    pipe = Pipeline(steps)
    return pipe


def optimize_param(pipeline, parameter_grid, data):
    # todo
    return None


def cross_validated_predictions(pipeline, parameters, data):
    # todo
    return None


def learn_model(pipeline, parameters):
    # todo
    return None
