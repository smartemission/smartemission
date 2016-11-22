from pandas import DataFrame, merge, Series, concat
from numpy.random import choice
from numpy import arange, sort, isnan
from sklearn.base import BaseEstimator, TransformerMixin


def running_mean(x, alpha, start):
    """
    Filters a series of observations by a running mean
    new mean = obs * alpha + `previous mean` * (1 - alpha)
    """
    val = start
    new_x = []
    for (i, elem) in enumerate(x):
        val = elem * alpha + val * (1.0 - alpha)
        new_x.append(val)
    return Series(new_x)


class Filter(BaseEstimator, TransformerMixin):
    """
    Pipeline element for sklearn
    Filter a column of the data with a running mean
    """

    def __init__(self, data, alpha, columns, sort_columns, start=0):
        self.x = data
        self.start = start
        self.alpha = alpha
        if type(columns) is not list:
            columns = [columns]
        self.columns = columns
        if type(sort_columns) is not list:
            sort_columns = [sort_columns]
        self.sort_columns = sort_columns

    def fit(self, x, y=None):
        self.x = self.x.sort_values(self.sort_columns)
        self.x.reset_index()
        for column in self.columns:
            a = running_mean(self.x[column], self.alpha, self.start)
            # self.x[column] = a
            self.x[column].update(a)
        return self

    def transform(self, x):
        col = self.columns + self.sort_columns
        x = x.drop(self.columns, axis=1)
        x = merge(x, self.x.loc[:, col], how='left', on=self.sort_columns)
        x = x.drop(self.sort_columns, axis=1)
        return x
