from stetl.component import Config
from stetl.filter import Filter
from stetl.packet import FORMAT
from stetl.util import Util

import matplotlib
matplotlib.use('Agg')
import pandas as pd

log = Util.get_log('Calibration')


class MergeRivmJose(Filter):
    """
    Merges Rivm and Jose timeseries records.
    """
    @Config(ptype=int, default=5, required=True)
    def impute_duration(self):
        """
        Number of minutes to impute data

        Default: 5

        Required: True
        """

    def __init__(self, configdict, section, consumes=FORMAT.record,
                 produces=FORMAT.record):
        Filter.__init__(self, configdict, section, consumes, produces)

    def invoke(self, packet):
        # Convert packet data to dataframes
        result_in = packet.data
        df_rivm = result_in['rivm']
        df_jose = result_in['jose']

        log.info('Received rivm data with shape (%d, %d)' % df_rivm.shape)
        log.info('Received jose data with shape (%d, %d)' % df_jose.shape)
        log.info('Pre-processing geohash and time')

        # Preparing Jose and RIVM data
        df_jose = MergeRivmJose.preproc_geohash_and_time(df_jose)
        df_rivm = MergeRivmJose.preproc_geohash_and_time(df_rivm)
        df_jose = MergeRivmJose.interpolate(df_jose, self.impute_duration * 5)

        # Concatenate RIVM and Jose
        df_index = df_jose.loc[:, ['time', 'geohash']]
        df_rivm = MergeRivmJose.interpolate_to_index(df_index, df_rivm, 60 * 5)
        df = pd.merge(df_jose, df_rivm, 'left', ['time', 'geohash'])
        del df.index.name
        log.info('RIVM and Jose are merged, new shape (%d, %d)' % df.shape)

        # Returning data
        # note: not converting to records, because that take a lot of memory.
        packet.data = {'merged': df}

        return packet

    @staticmethod
    def preproc_geohash_and_time(df):
        df['geohash'] = df['geohash'].str.slice(0, 7)
        df['time'] = pd.to_datetime(df['time'])
        return (df)

    @staticmethod
    def interpolate(df, impute_duration, limit_direction='both'):
        df = df.set_index(['geohash', 'time']).sort_index()
        df = df.interpolate(limit=impute_duration * 5,
                            limit_direction=limit_direction)
        df = df.reset_index()
        return df

    @staticmethod
    def interpolate_to_index(df_index, df_inter, impute_duration):
        log.info('Interpolating RIVM values towards jose measurements')
        df_index['is_index'] = True
        df = df_index.merge(df_inter, 'outer')
        df = MergeRivmJose.interpolate(df, impute_duration)
        df = df[df['is_index'].notnull()]
        df = df.drop('is_index', axis=1)
        return df

