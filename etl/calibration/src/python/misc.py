def merge_two_dicts(x, y):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    :param x:
    :param y:
    :return:
    """
    z = x.copy()
    z.update(y)
    return z
