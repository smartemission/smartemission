from stetl.filter import Filter
from stetl.packet import FORMAT

import pandas as pd


class MergeRivmJose(Filter):

    def __init__(self, configdict, section, consumes=FORMAT.record_array,
                 produces=FORMAT.record_array):
        Filter.__init__(self, configdict, section, consumes, produces)

    def invoke(self, packet):

        result_in = packet.data
        rivm = result_in['rivm']
        jose = result_in['jose']

        df_rivm = pd.DataFrame.from_records(rivm)
        df_jose = pd.DataFrame.from_records(jose)

        # todo rename columns and interpolate rivm
        df = pd.merge(df_jose, df_rivm, 'outer')

        packet.data = pd.DataFrame.to_records(df)

        return packet