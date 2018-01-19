import time
from calendar import timegm
from stetl.component import Config
from stetl.input import Input
from stetl.packet import FORMAT
from stetl.util import Util

from influxdb import InfluxDBClient

log = Util.get_log("InfluxDbInput")


class InfluxDbInput(Input):
    """
    InfluxDB TimeSeries (History) Input base class. Uses the
    `influxdb.InfluxDBClient`.
    """

    # Start attribute config meta
    @Config(ptype=str, required=False, default='localhost')
    def host(self):
        """
        host name or host IP-address, defaults to 'localhost'
        """
        pass

    @Config(ptype=str, required=False, default='8086')
    def port(self):
        """
        port (string) for host, defaults to '8086'
        """
        pass

    @Config(ptype=str, required=False, default='admin')
    def user(self):
        """
        User name, defaults to 'admin'
        """
        pass

    @Config(ptype=str, required=False, default='admin')
    def password(self):
        """
        User password, defaults to 'admin'
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
        Input.__init__(self, configdict, section, produces)
        self.client = None

    def init(self):
        log.info("Setting up connection to influxdb %s:%s, database=%s" %
                 (self.host, self.port, self.database))
        self.client = InfluxDBClient(self.host, self.port, self.user,
                                     self.password, self.database)

    def date_str_to_ts_nanos(self, date_str):
        # See https://aboutsimon.com/blog/2013/06/06/Datetime-hell-Time-zone-aware-to-UNIX-timestamp.html
        # e.g. 2017-11-17T11:00:00.411Z
        timestamp = timegm(
            time.strptime(
                date_str.replace('Z', 'GMT'),
                '%Y-%m-%dT%H:%M:%S.%f%Z'
            )
        )
        return timestamp

    def get_field_names(self, measurement):
        """
        Get Field names (columns) for Measurement.
        :param measurement:
        :return list of field names:
        """
        fields = self.query_db('SHOW FIELD KEYS FROM %s' % measurement)
        return [v['fieldKey'] for v in fields]

    def get_measurement_names(self):
        """

        :return list of Measurement names:
        """
        meas = self.query_db('SHOW MEASUREMENTS')
        return [v['name'] for v in meas]

    def get_start_time(self, measurement):
        """
        Get start date/time of Measurement.
        :param measurement: 
        :return tuple of: starttime as UTC string, timestamp in nanos: 
        """
        date_str = self.query_db('SELECT FIRST(%s), time FROM %s' %
                                 (self.get_field_names(measurement)[0], measurement))[0]['time']
        ts = self.date_str_to_ts_nanos(date_str)
        return date_str, ts

    def get_end_time(self, measurement):
        """
        Get end date/time of Measurement.
        :param measurement: 
        :return tuple of: endtime as UTC string, timestamp in nanos: 
        """
        date_str = self.query_db('SELECT LAST(%s), time FROM %s' %
                                 (self.get_field_names(measurement)[0], measurement))[0]['time']
        ts = self.date_str_to_ts_nanos(date_str)
        return date_str, ts

    def query_db(self, query):
        log.info("Querying database: %s", query)
        result = self.client.query(query)

        if result.error is not None:
            log.warning("Error while querying influxdb: %s", result.error)
            result_out = list()

        else:
            result_out = list(result.get_points())

        log.info("Received %s results" % len(result_out))

        return result_out

    def read(self, packet):
        result_out = self.query_db(self.query)
        packet.data = result_out
        packet.set_end_of_stream()
        return packet
