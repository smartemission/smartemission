import pandas as pd
from influxdb import DataFrameClient


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


def get_jose_data(host, port, user, password, dbname, series_name, limit=None):
    query = "SELECT * FROM %s" % series_name
    if limit is not None:
        query += " LIMIT %d" % limit

    client = DataFrameClient(host, port, user, password, dbname)
    client.switch_database(dbname)
    df = client.query(query)[series_name]
    return df


# if __name__ == '__main__':
#     print(get_jose_data("localhost", 8086, "pieter_reader", "pieter_pass",
#                   "smartemission", "joseextract", 10))
