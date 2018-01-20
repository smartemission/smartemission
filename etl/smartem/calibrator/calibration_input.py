from stetl.inputs.fileinput import FileInput
from stetl.component import Config
from stetl.packet import FORMAT
from stetl.util import Util

import pandas as pd
from smartem.influxdbinput import InfluxDbInput

log = Util.get_log('Calibration input')


class CalibrationInfluxDbInput(InfluxDbInput):
    """
    InfluxDB TimeSeries (History) Input, specific
    for reading calibration input data.
    """

    @Config(ptype=str, required=True)
    def key(self):
        """
        The key where the values are saved in the data

        Required: True
        """

    @Config(ptype=bool, default=False, required=True)
    def cache_result(self):
        """
        Whether or not to chache te result for a next call

        Default: False

        Required: True
        """

    def __init__(self, configdict, section):
        InfluxDbInput.__init__(self, configdict, section)
        self.last_timestamp = None
        self.df = None

    def before_invoke(self, packet):
        self.last_timestamp = '1900-01-01T00:00:00Z'

    def read(self, packet):
        results = packet.data
        if results is None:
            results = dict()

        if self.df is None or not self.cache_result:
            dfs = []
            while True:
                db_ret = self.query_db(self.query % self.last_timestamp)
                if len(db_ret) > 0:
                    self.last_timestamp = db_ret[-1]['time']
                    log.info('Last timestamp from influxdb is %s' % self.last_timestamp)
                    df = pd.DataFrame.from_records(db_ret)
                    df = df.pivot_table('value', ['geohash', 'time'],
                                        'component').reset_index()
                    dfs.append(df)
                else:
                    break
            self.df = pd.concat(dfs)

        results[self.key] = self.df

        packet.data = results
        packet.set_end_of_stream()

        return packet


class CalibrationDataInput(FileInput):
    def __init__(self, configdict, section, produces=FORMAT.record):
        FileInput.__init__(self, configdict, section, produces)

    def read_file(self, file_path):
        log.debug("Reading data from file")
        df = pd.DataFrame.from_csv(file_path)
        return {'merged': df}
