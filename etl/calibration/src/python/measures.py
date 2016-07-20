import numpy as np


def rmse(y, y_pred):
    """

    :param y:
    :type y: np.array
    :param y_pred:
    :type y_pred: np.array
    :return:
    """
    return np.sqrt(np.mean(np.power(y - y_pred, 2)))


def rmse_exp(y, y_pred):
    """

    :param y:
    :type y: np.array
    :param y_pred:
    :type y_pred: np.array
    :return:
    """
    return np.sqrt(np.mean(np.power(np.exp(y) - np.exp(y_pred), 2)))
