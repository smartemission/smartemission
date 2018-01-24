import time
from datetime import datetime
import json
from stetl.component import Config

from stetl.postgis import PostGIS
from stetl.util import Util

from smartem.influxdbinput import InfluxDbInput

log = Util.get_log("HarvesterInfluxDbInput")

NANOS_FACTOR = 1000 * 1000 * 1000


class HarvesterInfluxDbInput(InfluxDbInput):
    """
    InfluxDB TimeSeries (History) fetcher/formatter.

    Fetching all timeseries data from InfluxDB and putting
    these unaltered into recods e.g. for storing later in Postgres DB. This is a continuous process.
    Strategy is to use checkpointing: keep track of each sensor/timeseries how far we are
    in harvesting.

    Algorithm:

        * fetch all Measurements (table names)
        * for each Measurement:
        * if Measurement (name) is not in progress-table insert and set day,hour to 0
        * if in progress-table fetch entry (day, hour)
        * get timeseries (hours) available for that day
        * fetch and store each, starting with the last hour previously stored
        * ignore timeseries for current day/hour, as the hour will not be yet filled (and Refiner may else already process)
        * stored entry: measurement, day, hour, json blob
        * finish: when all done or when max_proc_time_secs passed
        
    """

    @Config(ptype=int, default=None, required=True)
    def max_proc_time_secs(self):
        """
        The maximum time in seconds we should continue processing input.

        Required: True

        Default: None
        """
        pass

    @Config(ptype=str, default=None, required=True)
    def device_type(self):
        """
        The station/device type, e.g. 'ase'.

        Required: False

        Default: None
        """
        pass

    @Config(ptype=str, default=None, required=True)
    def device_version(self):
        """
        The station/device version, e.g. '1'.

        Required: False

        Default: None
        """
        pass

    @Config(ptype=dict, default=None, required=False)
    def meas_name_to_device_id(self):
        """
        How to map InfluxDB Measurement (table) names to SE device id's.
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
        self.measurements_info = []
        self.index_m = -1
        self.query = "SELECT * FROM %s WHERE time >= %d AND time < %d + 1h"
        self.tracking_db = None

    def init(self):
        InfluxDbInput.init(self)

        # PostGIS for tracking Harvesting progress.
        # Tracking is automatically updated via a TRIGGER (see db-schema-raw).
        postgis_cfg = {'host': self.pg_host, 'port': self.pg_port, 'database': self.pg_database,
                       'user': self.pg_user, 'password': self.pg_password,
                       'schema': self.pg_schema
                       }
        self.tracking_db = PostGIS(postgis_cfg)
        self.tracking_db.connect()

        # One time: get all measurements and related info and store in structure
        measurements = self.get_measurement_names()
        for measurement in measurements:
            # Optional mapping from MEASUREMENT name to a device id
            # Otherwise device_is is Measurement name
            device_id = measurement
            if self.meas_name_to_device_id:
                if measurement not in self.meas_name_to_device_id:
                    log.error('No device_id mapped for measurement (table) %s' % measurement)
                    raise Exception

                device_id = self.meas_name_to_device_id[measurement]

            date_start_s, start_ts = self.get_start_time(measurement)
            date_end_s, end_ts = self.get_end_time(measurement)
            start_ts = self.date_str_to_whole_hour_nanos(date_start_s)
            end_ts *= NANOS_FACTOR

            # Shift time for current_ts from progress table if already in progress
            # otherwise use start time of measurement.
            current_ts = start_ts
            row_count = self.tracking_db.execute(self.progress_query + device_id)
            if row_count > 0:
                # Already in progress
                progress_rec = self.tracking_db.cursor.fetchone()
                ymd_last = str(progress_rec[4])
                year_last = ymd_last[0:4]
                month_last = ymd_last[4:6]
                day_last = ymd_last[6:]
                hour_last = progress_rec[5]
                # e.g. 2017-11-17T11:00:00.411Z
                date_str = '%s-%s-%sT%d:00:00.000Z' % (year_last, month_last, day_last, hour_last)
                current_ts = self.date_str_to_whole_hour_nanos(date_str)
                # skip to next hour
                # current_ts += (3600 * NANOS_FACTOR)

            # Store all info per device (measurement table) in list of dict
            self.measurements_info.append({
                'name': measurement,
                'date_start_s': date_start_s,
                'start_ts': start_ts,
                'date_end_s': date_end_s,
                'end_ts': end_ts,
                'current_ts': current_ts,
                'device_id': device_id
            })

        print ("measurements_info: %s" % str(self.measurements_info))

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

    # def next_whole_hour_from_date(self, date):
    #     date_s = self.query_db('SELECT FIRST(calibrated), time FROM %s' % measurement)[0]['time']
    #     return parser.parse(date_s)

    def date_str_to_whole_hour_nanos(self, date_str):
        """
        COnvert URZ date time string to timestamp nanos on whole hour.
        :param date_str:
        :return:
        """
        timestamp = self.date_str_to_ts_nanos(date_str)

        # print(timestamp)
        # Shift timestamp to next whole hour
        timestamp = (timestamp - (timestamp % 3600)) * NANOS_FACTOR
        # d = datetime.utcfromtimestamp(timestamp)
        # print('-> %s' % d.isoformat())
        return timestamp

    def read(self, packet):
        measurement_info = self.next_measurement_info()

        current_ts_nanos = measurement_info['current_ts']
        current_ts_secs = current_ts_nanos / NANOS_FACTOR
        query = self.query % (measurement_info['name'], current_ts_nanos, current_ts_nanos)
        data = self.query_db(query)

        if len(data) >= 1:
            d = datetime.utcfromtimestamp(current_ts_secs)
            day = d.strftime('%Y%m%d')
            hour = str(d.hour + 1).zfill(2)

            # DEBUG: store only first and last of hour-series
            data_first = {
                'time': data[0]['time']
            }
            data_last = {
                'time': data[len(data) - 1]['time']
            }
            # data_o = data
            # data = [data_first, data_last]
            # for i in range(0,4):
            #     data.append(data_o[i])

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
        record['device_type'] = self.device_type
        record['device_version'] = self.device_version
        record['day'] = day
        record['hour'] = hour

        # Determine if hour is "complete"
        record['complete'] = False
        d = datetime.utcfromtimestamp(self.current_time_secs())
        cur_day = int(d.strftime('%Y%m%d'))
        cur_hour = d.hour + 1
        if cur_day > int(day) \
                or (cur_day == int(day) and cur_hour > int(hour)):
            record['complete'] = True

        # Optional prefix for each param, usually sensor-box type e.g. "ase_"
        # if self.data_param_prefix:
        #     for data_elm in data:
        #         keys = data_elm.keys()
        #         # https://stackoverflow.com/questions/4406501/change-the-name-of-a-key-in-dictionary
        #         for key in keys:
        #             data_elm[self.data_param_prefix + key] = data_elm.pop(key)

        # Add JSON text blob
        record['data'] = json.dumps({
            'id': device_id,
            'date': day,
            'hour': hour,
            'timeseries': data
        })

        return record
