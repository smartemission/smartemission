from stetl.component import Config
from stetl.filter import Filter
from stetl.packet import FORMAT
from stetl.util import Util

import pandas as pd

log = Util.get_log("Calibration")


class MergeRivmJose(Filter):

    @Config(ptype=dict, required=True)
    def map_jose(self):
        """
        Mapping between Jose stations and "location id's"

        Required: True
        """

    @Config(ptype=dict, required=True)
    def map_rivm(self):
        """
        Mapping between RIVM stations and "location id's"

        Required: True
        """

    def __init__(self, configdict, section, consumes=FORMAT.record_array,
                 produces=FORMAT.record_array):
        Filter.__init__(self, configdict, section, consumes, produces)

    def invoke(self, packet):

        # Convert packet data to dataframes
        result_in = packet.data
        rivm = result_in['rivm']
        jose = result_in['jose']
        df_rivm = pd.DataFrame.from_records(rivm)
        df_jose = pd.DataFrame.from_records(jose)

        # Rename stations
        df_jose = df_jose.replace({'station': self.map_jose})
        df_rivm = df_rivm.replace({'station': self.map_rivm})

        # Set time as index
        df_rivm['time'] = pd.to_datetime(df_rivm['time'])
        df_jose['time'] = pd.to_datetime(df_jose['time'])

        # Interpolate RIVM to jose times
        jose_index = df_jose['time'].unique()
        jose_time = pd.DataFrame({'time': jose_index})
        df_rivm = jose_time.merge(df_rivm, 'outer').set_index('time')
        df_rivm = df_rivm.sort_index().interpolate().ffill().loc[jose_index]

        # Pivot Jose
        df_jose = df_jose.pivot_table('value', ['station', 'time'],
                                      'component').reset_index()

        # Concatenate RIVM and Jose
        df_rivm = df_rivm.reset_index()
        df_jose = df_jose.reset_index()
        df = pd.merge(df_rivm, df_jose, 'outer', ['time', 'station'])

        log.info(df.describe())
        log.info(df.info())

        # Select rows and columns
        del df['component']
        del df['index']

        # df = df.dropna()

        # log.info("==JOSE==")
        # log.info("\n" + str(df_jose))
        # log.info(type(df_jose))
        # log.info("\n" + str(df_jose.dtypes))
        # log.info(df_jose.columns)
        #
        # log.info("==RIVM==")
        # log.info("\n" + str(df_rivm))
        # log.info(type(df_rivm))
        # log.info("\n" + str(df_rivm.dtypes))
        # log.info(df_rivm.columns)
        #
        # log.info("==DF==")
        # log.info("\n" + str(df))
        # log.info(type(df))
        # log.info("\n" + str(df.dtypes))
        # log.info(df.columns)

        packet.data = df.to_dict('records')

        return packet