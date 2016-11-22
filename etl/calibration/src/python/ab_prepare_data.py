from numpy import abs, nan, arange
from numpy.random import choice


def prepare_rivm(df):
    co_avg = df.CO_Waarden.mean()
    co_std = df.CO_Waarden.std()
    df[abs(df.CO_Waarden - co_avg) <= (10 * co_std)] = nan
    return df


def prepare_jose(df):
    return df


def combine_rivm_and_jose(df_rivm, df_jose, col_predict):
    cols_predict = ['O3_Waarden', 'NO2_Waarden', 'CO_Waarden']
    df = df_rivm.drop([i for i in cols_predict if i != col_predict], 1)
    df = df.dropna()

    return df


    # def get_rivm_and_jose_data_from_file(col_predict, n_part, train_file, verbose):
    # x_all, y_all, x, y = get_data(FOLDER_DATA, train_file, col_predict, n_part)
    #     if verbose > 0: print('Using %d data points from now on' % x.shape[0])
    #     return x, x_all, y, y_all

def get_learn_and_validate_sample(df, ratio):
    n_rows = df.shape[0]
    idx = choice(arange(0, n_rows), int(n_rows * ratio))
    return df.iloc[idx, :]


def split_data_label(df, label):
    y = df[label]
    x = df.drop(label, axis = 1)
    return x, y