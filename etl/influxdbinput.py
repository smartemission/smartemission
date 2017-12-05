import time
from calendar import timegm
from dateutil import parser
from datetime import datetime, timedelta
import json
from stetl.component import Config
from stetl.inputs.dbinput import DbInput
from stetl.packet import FORMAT
from stetl.postgis import PostGIS
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
                                     self.password, self.database)

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

NANOS_FACTOR = 1000 * 1000 * 1000

class HarvesterInfluxDbInput(InfluxDbInput):
    """
    InfluxDB TimeSeries (History) fetcher/formatter.

    Fetching all timeseries data from InfluxDB and putting
    these unaltered into Postgres DB. This is a continuus process.
    Strategy is to use checkpointing: keep track of each sensor/timeseries how far we are
    in harvesting.

    Algoritm:
    - fetch all Measurements (table names)
    - for each Measurement:
    - if Measurement (name) is not in progress-table insert and set day,hour to 0
    - if in progress-table fetch entry (day, hour)
    - get timeseries (hours) available for that day
    - fetch and store each, starting with the last hour previously stored
    - ignore timeseries for current day/hour, as the hour will not be yet filled (and Refiner may else already process)
    - stored entry: measurement, day, hour, json blob
    - finish: when all done or when max_proc_time_secs passed
    """

    @Config(ptype=int, default=None, required=True)
    def max_proc_time_secs(self):
        """
        The maximum time in seconds we should continue processing input.

        Required: True

        Default: None
        """
        pass

    @Config(ptype=str, default=None, required=False)
    def data_param_prefix(self):
        """
        The prefix string to place before each parameter name in data, e.g. 'ase_'.

        Required: False

        Default: None
        """
        pass

    @Config(ptype=dict, default=None, required=False)
    def meas_name_to_device_id(self):
        """
        How to map InfluxDB Measurement names to SE device id's.
        e.g. {'Geonovum1' : '1181001', 'RIVM2' : '1181002'}

        Required: False

        Default: None
        """
        pass

    @Config(ptype=str, default=None, required=True)
    def progress_table(self):
        """
        The Postgres table tracking all last processed days/hours for each device.

        Required: True

        Default: None
        """
        pass

    @Config(ptype=str, required=False, default='localhost')
    def pg_host(self):
        """
        host name or host IP-address, defaults to 'localhost'
        """
        pass

    @Config(ptype=str, required=False, default='5432')
    def pg_port(self):
        """
        port for host, defaults to '5432'
        """
        pass

    @Config(ptype=str, required=True)
    def pg_database(self):
        """
        database name
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def pg_user(self):
        """
        User name, defaults to 'postgres'
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def pg_password(self):
        """
        User password, defaults to 'postgres'
        """
        pass

    @Config(ptype=str, required=False, default='public')
    def pg_schema(self):
        """
        The postgres schema name, defaults to 'public'
        """
        pass

    def __init__(self, configdict, section):
        InfluxDbInput.__init__(self, configdict, section)
        self.current_time_secs = lambda: int(round(time.time()))
        self.start_time_secs = self.current_time_secs()
        self.progress_query = "SELECT * from %s where device_id=" % self.progress_table
        self.measurements = None
        self.measurements_info = []
        self.index_m = -1
        self.query = "SELECT * FROM %s WHERE time >= %d AND time < %d + 1h"

    def init(self):
        InfluxDbInput.init(self)
        postgis_cfg = {'host': self.pg_host, 'port': self.pg_port, 'database': self.pg_database,
                       'user': self.pg_user, 'password': self.pg_password,
                       'schema': self.pg_schema
                       }
        self.db = PostGIS(postgis_cfg)
        self.db.connect()

        # One time: get all measurements and related info and store in structure
        self.measurements = self.query_db('SHOW MEASUREMENTS')
        for measurement in self.measurements:
            measurement_name = measurement['name']
            date_start_s = self.query_db('SELECT FIRST(calibrated), time FROM %s' % measurement_name)[0]['time']
            start_ts = self.date_str_to_ts_nanos(date_start_s)
            date_end_s = self.query_db('SELECT LAST(calibrated), time FROM %s' % measurement_name)[0]['time']
            end_ts = self.date_str_to_ts_nanos(date_end_s)
            device_id = measurement_name
            if self.meas_name_to_device_id:
                if measurement_name not in self.meas_name_to_device_id:
                    log.error('No device_id mapped for measurement (table) %s' % measurement_name)
                    raise Exception

                device_id = self.meas_name_to_device_id[measurement_name]


            # Shift time for current_ts from progress table if already in progress
            # otherwise use start time of measurement.
            current_ts = start_ts
            row_count = self.db.execute(self.progress_query + device_id)
            if row_count > 0:
                progress_rec = self.db.cursor.fetchone()
                ymd_last = str(progress_rec[4])
                year_last = ymd_last[0:4]
                month_last = ymd_last[4:6]
                day_last = ymd_last[6:]
                hour_last = progress_rec[5]
                # e.g. 2017-11-17T11:00:00.411Z
                date_str = '%s-%s-%sT%d:00:00.0Z' % (year_last, month_last, day_last, hour_last)
                current_ts = self.date_str_to_ts_nanos(date_str)
                # skip to next hour
                current_ts += (3600 * NANOS_FACTOR)
                
            # Store all info per device (measurement table) in list of dict
            self.measurements_info.append({
                'name': measurement_name,
                'date_start_s': date_start_s,
                'start_ts': start_ts,
                'date_end_s': date_end_s,
                'end_ts': end_ts,
                'current_ts': current_ts,
                'device_id': device_id
            })

        print (str(self.measurements_info))
        
    def all_done(self):
        return len(self.measurements_info) == 0

    def has_expired(self):
        if (self.current_time_secs() - self.start_time_secs) > self.max_proc_time_secs:
            return True
        return False

    def next_measurement_info(self):
        self.index_m += 1
        return self.measurements_info[self.index_m % len(self.measurements_info)]

    def del_measurement_info(self):
        if not self.all_done():
            del self.measurements_info[self.index_m % len(self.measurements_info)]

    def before_invoke(self, packet):
        if self.has_expired() or self.all_done():
            # All devices read or timer expiry
            log.info('Processing halted: expired or all done')
            packet.set_end_of_stream()
            return False

    def date_str_to_ts_nanos(self, date_str):
        # See https://aboutsimon.com/blog/2013/06/06/Datetime-hell-Time-zone-aware-to-UNIX-timestamp.html
        # e.g. 2017-11-17T11:00:00.411Z
        timestamp = timegm(
            time.strptime(
                date_str.replace('Z', 'GMT'),
                '%Y-%m-%dT%H:%M:%S.%f%Z'
            )
        )

        # print(timestamp)
        # Shift timestamp to next whole hour
        timestamp = (timestamp - (timestamp % 3600) + 3600) * NANOS_FACTOR
        # d = datetime.utcfromtimestamp(timestamp)
        # print('-> %s' % d.isoformat())
        return timestamp

    # def next_whole_hour_from_date(self, date):
    #     date_s = self.query_db('SELECT FIRST(calibrated), time FROM %s' % measurement)[0]['time']
    #     return parser.parse(date_s)

    def read(self, packet):
        measurement_info = self.next_measurement_info()

        current_ts_nanos = measurement_info['current_ts']
        current_ts_secs = current_ts_nanos/NANOS_FACTOR
        query = self.query % (measurement_info['name'], current_ts_nanos, current_ts_nanos)
        data = self.query_db(query)
        
        if len(data) >= 1:
            d = datetime.utcfromtimestamp(current_ts_secs)
            day = '%d%d%d' % (d.year, d.month, d.day)
            hour = '%d' % (d.hour+1)
            # DEBUG: store only first and last of hour-series
            # data_first = data[0]
            # data_last = data[len(data)-1]
            data_o = data
            data = []
            for i in range(0,24):
                data.append(data_o[i])
            # data.append(data_first)
            # data.append(data_last)
            packet.data = self.format_data(measurement_info['device_id'], day, hour, data)

        # Shift time an hour for this device
        current_ts_nanos = (current_ts_secs + 3600) * NANOS_FACTOR
        if current_ts_nanos > measurement_info['end_ts']:
            # all done for current measurement/device
            self.del_measurement_info()
        else:
            # Shift to next hour for this measurement
            measurement_info['current_ts'] = current_ts_nanos
                        
        return packet

    # Create a data record for timeseries of current device/day/hour
    def format_data(self, device_id, day, hour, data):

        #
        # -- Map this to
        # CREATE TABLE smartem_raw.timeseries (
        #   gid serial,
        #   unique_id character varying (16),
        #   insert_time timestamp with time zone default current_timestamp,
        #   device_id integer,
        #   day integer,
        #   hour integer,
        #   data json,
        #   complete boolean default false,
        #   PRIMARY KEY (gid)
        # );


        # Create record with JSON text blob with metadata
        record = dict()
        record['unique_id'] = '%s-%s-%s' % (device_id, day, hour)

        # Timestamp of sample
        record['device_id'] = device_id
        record['day'] = day
        record['hour'] = hour

        # Optional prefix for each param, usually sensor-box type e.g. "ase_"
        if self.data_param_prefix:
            for data_elm in data:
                keys = data_elm.keys()
                # https://stackoverflow.com/questions/4406501/change-the-name-of-a-key-in-dictionary
                for key in keys:
                    data_elm[self.data_param_prefix + key] = data_elm.pop(key)
                
        # Add JSON text blob
        record['data'] = json.dumps({
            'id': device_id,
            'date': day,
            'hour': hour,
            'timeseries': data
        })

        return record
