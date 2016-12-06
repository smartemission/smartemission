import pandas as pd


def get_rivm_and_jose_data_from_prepared_file(path):
    return pd.read_csv(path)


def get_rivm_and_jose_data(path=None):
    if path is None:
        path = path_prepared_file
    # df_rivm = get_rivm_data()
    # df_jose = get_jose_data()
    # return df_rivm, df_jose
    return get_rivm_and_jose_data_from_prepared_file(path), None


def get_rivm_data():
    pass


def get_jose_data():
    pass
