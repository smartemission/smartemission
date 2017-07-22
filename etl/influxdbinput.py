from stetl.component import Config
from stetl.inputs.dbinput import DbInput
from stetl.packet import FORMAT
from stetl.util import Util

import pandas as pd
from influxdb import InfluxDBClient

log = Util.get_log("InfluxDbInput")


class InfluxDbInput(DbInput):
    # Start attribute config meta
    @Config(ptype=str, required=False, default='localhost')
    def host(self):
        """
        host name or host IP-address, defaults to 'localhost'
        """
        pass

    @Config(ptype=str, required=False, default='5432')
    def port(self):
        """
        port for host, defaults to '5432'
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def user(self):
        """
        User name, defaults to 'postgres'
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def password(self):
        """
        User password, defaults to 'postgres'
        """
        pass

    @Config(ptype=str, required=True)
    def database(self):
        """
        The "database" is a db-like entity in an InfluxDB server instance.

        Required: True

        Default: N.A.
        """
        pass

    @Config(ptype=str, required=True)
    def query(self):
        """
        The query for the database

        Required: True
        """

    def __init__(self, configdict, section, produces=FORMAT.record_array):
        DbInput.__init__(self, configdict, section, produces)
        self.client = None

    def init(self):
        log.info("Setting up connection to influxdb %s:%s, database=%s" %
                 (self.host, self.port, self.database))
        self.client = InfluxDBClient(self.host, self.port, self.user,
                                     self.password, self.database, timeout=300, retries=10)

    @staticmethod
    def normalize_aggreagete_result(result):
        result_out = []
        for key, values in result.items():
            grouping = key[1]
            for value in values:
                for group, group_value in grouping.items():
                    value[group] = group_value
                result_out.append(value)
        return result_out

    def query_db(self, query):
        log.info("Querying database: %s", query)
        result = self.client.query(query)

        if result.error is not None:
            log.warning("Error while querying influxdb: %s", result.error)
            result_out = list()

        else:
            if 'group by' not in self.query.lower():
                result_out = list(result.get_points())
            else:
                result_out = InfluxDbInput.normalize_aggreagete_result(result)

        log.info("Received %s results" % len(result_out))

        return result_out

    def read(self, packet):
        result_out = self.query_db(self.query)
        packet.data = result_out
        packet.set_end_of_stream()
        return packet


class CalibrationInfluxDbInput(InfluxDbInput):

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

    @Config(ptype=str, default='1900-01-01', required=False)
    def lower_time_limit(self):
        """
        The lower time limit for the query.
        
        Default: '1900-01-01'
        
        Required: False
        """

    @Config(ptype=int, default=0, required=False)
    def min_n(self):
        """
        Minimum number of samples. Compares with the `n` field in the result. If 0 nothing is done. 
        
        Default: 0 (do nothing)
        
        Required: False
        """

    def __init__(self, configdict, section):
        InfluxDbInput.__init__(self, configdict, section)
        self.last_timestamp = None
        self.df = None

    def before_invoke(self, packet):
        self.last_timestamp = self.lower_time_limit

    def read(self, packet):
        results = packet.data
        if results is None:
            results = dict()

        if self.df is None or not self.cache_result:
            db_ret = self.query_db(self.query % self.last_timestamp)
            self.last_timestamp = db_ret[-1]['time']
            log.info('Last timestamp from influxdb is %s' % self.last_timestamp)
            df = pd.DataFrame.from_records(db_ret)

            if self.min_n > 0:
                df = df[df['n'] > self.min_n]

            self.df = df.pivot_table('value', ['geohash', 'time'],
                                'component').reset_index()

        results[self.key] = self.df

        packet.data = results
        packet.set_end_of_stream()

        return packet
