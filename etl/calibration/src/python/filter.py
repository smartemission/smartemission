import pandas as pd
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
    return pd.Series(new_x)


class Filter(BaseEstimator, TransformerMixin):
    """
    Pipeline element for sklearn
    Filter a column of the data with a running mean
    """

    def __init__(self, x, alpha, columns, sort_column, start=0):
        self.x = x
        self.start = start
        self.alpha = alpha
        self.columns = columns
        self.sort_column = sort_column

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        cols = list(self.columns)
        new_x = pd.DataFrame.from_records(self.x)
        new_x = new_x.sort_values(self.sort_column)
        for column in cols:
            new_x[column] = running_mean(new_x.loc[:, column], self.alpha,
                                         self.start)
        col = cols + [self.sort_column]
        x = x.drop(cols, axis=1)
        x = pd.merge(x, new_x.loc[:, col], how='left', on=self.sort_column)
        return x
