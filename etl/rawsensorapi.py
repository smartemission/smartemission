# -*- coding: utf-8 -*-
#
# RawSensorInput: fetch raw values from CityGIS Raw Sensor REST API.
#
# Author:Just van den Broecke

import json
import time
from datetime import datetime, timedelta
from stetl.component import Config
from stetl.util import Util
from stetl.inputs.httpinput import HttpInput
from stetl.packet import FORMAT
from stetl.postgis import PostGIS
from sensordefs import *

log = Util.get_log("RawSensorAPI")


class RawSensorAPIInput(HttpInput):
    """
    Raw Sensor REST API (CityGIS) Base Class to fetch observations for devices.
    """

    @Config(ptype=int, default=0, required=False)
    def api_interval_secs(self):
        """
        The time in seconds to wait before invoking the RSA API again.

        Required: True

        Default: 0
        """
        pass

    def __init__(self, configdict, section, produces=FORMAT.record_array):
        HttpInput.__init__(self, configdict, section, produces)

        # Init all device id's
        self.device_ids = []
        self.device_ids_idx = -1
        self.device_id = -1

        # Save the Base URL, specific URLs will be constructed in self.url later
        self.base_url = self.url
        self.url = None

    def init(self):
        pass

    def fetch_devices(self):
        self.device_ids_idx = -1
        self.device_ids = []
        self.device_id = -1

        devices_url = self.base_url + '/devices'
        log.info('Init: fetching device list from URL: "%s" ...' % devices_url)
        json_str = self.read_from_url(devices_url)
        json_obj = self.parse_json_str(json_str)
        device_urls = json_obj['devices']

        # We need just the device id's
        # array element is like "/sensors/v1/devices/8", so cut out the id
        for d in device_urls:
            self.device_ids.append(int(d.split('/')[-1]))

        if len(self.device_ids) > 0:
            self.device_ids_idx = 0

        log.info('Found %4d devices: %s' % (len(self.device_ids), str(self.device_ids)))

    def before_invoke(self, packet):
        """
        Called just before Component invoke.
        """
        return True

    def after_invoke(self, packet):
        """
        Called just after Component invoke.
        """

        # just pause to not overstress the RSA
        if self.api_interval_secs > 0:
            time.sleep(self.api_interval_secs)

        return True

    def exit(self):
        # done
        log.info('Exit')

    def next_entry(self, a_list, idx):
        if len(a_list) == 0 or idx >= len(a_list):
            idx = -1
            entry = -1
        else:
            entry = a_list[idx]
            idx += 1

        return entry, idx

    def parse_json_str(self, raw_str):
        # Parse JSON from data string
        json_obj = None
        try:
            json_obj = json.loads(raw_str)
        except Exception, e:
            log.error('Cannot parse JSON from %s, err= %s' % (raw_str, str(e)))
            raise e

        return json_obj


class RawSensorLastInput(RawSensorAPIInput):
    """
    Raw Sensor REST API (CityGIS) to fetch last values for all devices.
    """

    @Config(ptype=list, default=[], required=True)
    def sensor_names(self):
        """
        The output sensor names to refine.

        Required: True

        Default: []
        """
        pass

    def __init__(self, configdict, section, produces=FORMAT.record_array):
        RawSensorAPIInput.__init__(self, configdict, section, produces)


    def init(self):
        # One time: get all device ids
        self.fetch_devices()

    def before_invoke(self, packet):
        """
        Called just before Component invoke.
        """

        # The base method read() will fetch self.url until it is set to None
        self.device_id, self.device_ids_idx = self.next_entry(self.device_ids, self.device_ids_idx)

        # Stop when all devices done
        if self.device_id < 0:
            self.url = None
            log.info('Processing halted: all devices done')
            packet.set_end_of_stream()
            return False

        # ASSERT: still device(s) to be fetched

        # Set the next "last values" URL for device and increment to next
        self.url = self.base_url + '/devices/%d/last' % self.device_id

        return True

    # Convert observations to array of records, one for each designated (see self.outputs) output
    def format_data(self, data):

        # Convert/split response into an array of device_output records
        # {u'p_basetimer': 6,
        # u'p_coheatermode': 184549611,
        # u'v_audioplus9': 2960427, u'v_audioplus8': 2763049, u's_audioplus4': 2368291,
        # u's_audioplus2': 2433311, u'v_audioplus3': 2302754, u'v_audioplus2': 2236447, u'v_audioplus1': 2171422,
        # u'v_audioplus7': 2631462, u'v_audioplus6': 2434084, u'v_audioplus5': 2631463, u'v_audioplus4': 2368034,
        # u't_audioplus2': 2434339,
        # u'p_errorstatus': 0,
        # u's_rain': 0, u'id': u'25',
        # u's_lightsensorbottom': 0, u't_audioplus4': 2565414, u'p_11': 35253,
        # u's_temperatureunit': 289400,
        # u'p_unitserialnumber': 25,
        # u't_audioplus7': 2959143, u'p_17': 184549867, u'p_18': 184549867, u'p_19': 167772308,
        # u't_audioplus6': 2500133, u'u_audio0': 1645568, u's_coresistance': 362528, u's_rgbcolor': 16771796,
        # u's_audioplus8': 2828841, u's_lightsensorgreen': 11, u'p_totaluptime': 1741354, u'p_sessionuptime': 310354,
        # u't_audioplus8': 2828842, u's_co': 35936, u's_satinfo': 99082,
        # u's_latitude': 54345494, u't_audioplus1': 2369314,
        # u's_audioplus1': 2368543, u't_audioplus3': 2434086, u's_audioplus3': 2434083, u't_audioplus5': 2697512,
        # u's_audioplus5': 2697000, u's_audioplus6': 2434085, u's_audioplus7': 2762535, u't_audioplus9': 2960684,
        # u's_audioplus9': 2960427, u'u_audioplus5': 2500133, u'p_powerstate': 1935, u'p_temporarilyenablebasetimer': 1,
        # u's_o3': 39, u's_rtcdate': 1056819, u's_no2resistance': 549228, u's_barometer': 101788, u't_audio0': 2435072,
        # u's_temperatureambient': 275962, u's_secondofday': 64127, u's_lightsensorblue': 10, u's_acceleroy': 527,
        # u's_accelerox': 510, u's_humidity': 77961, u's_acceleroz': 763, u's_audio0': 1842688, u's_no2': 32,
        # u's_longitude': 6113060, u'v_audio0': 1908736, u's_lightsensortop': 15, u's_co2': 418000,
        # u'p_controllerreset': 322372921, u's_rtctime': 1126447, u'u_audioplus2': 1974301, u'u_audioplus3': 2170401,
        # u'u_audioplus1': 1974556, u'u_audioplus6': 2433828, u'u_audioplus7': 2565925, u'u_audioplus4': 2171169,
        # u'time': u'2016-02-03T16:47:51.3844629Z', u'u_audioplus8': 2763049, u'u_audioplus9': 2960427,
        # u's_lightsensorred': 12, u's_o3resistance': 414489}
        #
        # -- Map this to
        # CREATE TABLE smartem_rt.device_output (
        # gid serial,
        # unique_id character varying (16),
        # insert_time timestamp default current_timestamp,
        # device_id integer,
        # device_name character varying (32),
        # id integer,
        # name character varying,
        # label character varying,
        # unit  character varying,
        # time timestamp,
        # value_raw integer,
        # value_stale integer,
        # value real,
        # altitude integer default 0,
        # point geometry(Point,4326),
        # PRIMARY KEY (gid)
        # );
        
        # Parse JSON from data string fetched by base method read()
        sensor_vals = self.parse_json_str(data)
        if 'p_unitserialnumber' not in sensor_vals:
            return []

        sensor_name = 'none'
        device_id = int(sensor_vals['p_unitserialnumber'])
        records_out = []

        # Go through all the configured sensor outputs we need to calc values for
        # Do the conversion/calibration in 3 steps
        # 1) check inputs (available and valid)
        # 2) convert
        # 3) check output (available and valid)
        for sensor_name in self.sensor_names:
            record = None
            try:
                if sensor_name not in SENSOR_DEFS:
                    log.warn('Sensor name %s not defined in SENSOR_DEFS' % sensor_name)
                    continue

                sensor_def = SENSOR_DEFS[sensor_name]
                if 'input' not in sensor_def or 'converter' not in sensor_def:
                    continue

                # get raw input value(s)
                # i.e. in some cases multiple inputs are required (e.g. audio bands)
                input_name = sensor_def['input']
                input_valid, reason = check_value(input_name, sensor_vals)
                if not input_valid:
                    log.warn('device_id=%d sensor=%s: invalid input for %s: detail=%s' % (
                    device_id, sensor_name, str(input_name), reason))
                    continue

                value_raw = get_raw_value(input_name, sensor_vals)
                if value_raw is None:
                    # No use to proceed without raw input value(s)
                    continue

                # Start new record with common data
                record = {}
                record['name'] = sensor_name
                record['device_id'] = device_id
                record['device_name'] = 'station %d' % device_id
                record['label'] = sensor_def['label']
                record['unit'] = sensor_def['unit']
                record['unique_id'] = '%d-%s' % (device_id, record['name'])

                # Point location TODO: average, but for now assume static
                if 's_longitude' in sensor_vals and 's_latitude' in sensor_vals:
                    lon = SENSOR_DEFS['longitude']['converter'](sensor_vals['s_longitude'])
                    lat = SENSOR_DEFS['latitude']['converter'](sensor_vals['s_latitude'])

                    valid, reason = check_value('latitude', sensor_vals, value=lat)
                    if not valid:
                        continue

                    valid, reason = check_value('longitude', sensor_vals, value=lon)
                    if not valid:
                        continue

                    # Both lat and lon are valid!
                    record['point'] = 'SRID=4326;POINT(%f %f)' % (lon, lat)

                # No 'point' proceeding without a location
                if 'point' not in record:
                    continue

                # GPS height. TODO use air pressure
                record['altitude'] = 0
                if 's_altimeter' in sensor_vals:
                    altitude = SENSOR_DEFS['altitude']['converter'](sensor_vals['s_altimeter'])
                    valid, reason = check_value('altitude', sensor_vals, value=altitude)
                    if not valid:
                        altitude = 0

                    #  altitude valid!
                    record['altitude'] = altitude

                # Calculate values
                record['value_raw'] = value_raw

                value = sensor_def['converter'](value_raw, sensor_vals, sensor_name)
                output_valid, reason = check_value(sensor_name, sensor_vals, value=value)
                if not output_valid:
                    log.warn('id=%d-%s  invalid output for %s: detail=%s' % (
                    device_id, sensor_name, sensor_name, reason))
                    record = None
                    continue

                # Unix timestamp to calculate "stale state (0/1)" i.e. if a station has been
                # active over the last N hours (now 2). We keep all last values but flag inactive stations.
                record['time'] = convert_timestamp(sensor_vals['time'])
                utc_then = datetime.utcnow() - timedelta(hours=2)
                tstamp_sample = time.mktime(record['time'].timetuple())
                tstamp_then = time.mktime(utc_then.timetuple())
                record['value_stale'] = 0
                if tstamp_sample < tstamp_then:
                    record['value_stale'] = 1

                # Calculated value
                record['value'] = int(round(value))

            except Exception, e:
                log.error('Exception refining %s dev=%d, err=%s' % (sensor_name, device_id, str(e)))
            else:
                # No error and output value: assign record to result list
                if record and 'value' in record:
                    records_out.append(record)

        return records_out


class RawSensorTimeseriesInput(RawSensorAPIInput):
    """
    Raw Sensor REST API (CityGIS) to fetch (harvest) all timeseries for all devices.
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
    def progress_table(self):
        """
        The Postgres table tracking all last processed days/hours for each device.

        Required: True

        Default: None
        """
        pass

    """
    Raw Sensor REST API (CityGIS) TimeSeries (History) fetcher/formatter.
    
    Fetching all timeseries data via the Raw Sensor API (RSA) from CityGIS server and putting 
    these unaltered into Postgres DB. This is a continuus process.
    Strategy is to use checkpointing: keep track of each sensor/timeseries how far we are
    in harvesting.
    
    Algoritm:
    - fetch all (sensor) devices from RSA
    - for each device:
    - if device is not in progress-table insert and set day,hour to 0
    - if in progress-table fetch entry (day, hour)
    - get timeseries (hours) available for that day
    - fetch and store each, starting with the last hour perviously stored (as it may not be completely filled)
    - stored entry: device_id, day, hour, last_flag, json blob
    - finish: when all done or when max_proc_time_secs passed 
    """

    def __init__(self, configdict, section, produces=FORMAT.record_array):
        RawSensorAPIInput.__init__(self, configdict, section, produces)
        
        # keep track of root base REST URL
        self.url = None
        
        self.current_time_secs = lambda: int(round(time.time()))
        self.start_time_secs = self.current_time_secs()

        self.days = []
        self.days_idx = -1
        self.day = -1
        self.day_last = -1

        self.hours = []
        self.hours_idx = -1
        self.hour = -1
        self.hour_last = -1
        self.db = None

        self.progress_query = "SELECT * from %s where device_id=" % self.progress_table

    def init(self):
        self.db = PostGIS(self.cfg.get_dict())
        self.db.connect()

        # One time: get all device ids
        self.fetch_devices()

        # Pick a first device id
        # self.device_id, self.device_ids_idx = self.next_entry(self.device_ids, self.device_ids_idx)

    def all_done(self):
        if self.device_ids_idx < 0 and self.days_idx < 0 and self.hours_idx < 0:
            return True
        return False

    def has_expired(self):
        if (self.current_time_secs() - self.start_time_secs) > self.max_proc_time_secs:
            return True
        return False

    def fetch_ts_days(self):
        self.days_idx = -1
        self.days = []
        self.day = -1

        if self.device_id < 0:
            return
        
        ts_days_url = self.base_url + '/devices/%d/timeseries' % self.device_id
        log.info('Init: fetching timeseries days list from URL: "%s" ...' % ts_days_url)

        json_str = self.read_from_url(ts_days_url)
        json_obj = self.parse_json_str(json_str)

        # Typical entry is: "/sensors/v1/devices/8/timeseries/20160404"
        # cut of last
        days_raw = json_obj['days']

        row_count = self.db.execute(self.progress_query + str(self.device_id))
        self.day_last = -1
        self.hour_last = -1
        if row_count > 0:
            progress_rec = self.db.cursor.fetchone()
            self.day_last = progress_rec[4]
            self.hour_last = progress_rec[5]

        # Take a subset of all days: namely those still to be processed
        # Always include the last/current day as it may not be complete
        for d in days_raw:
            day = int(d.split('/')[-1])
            if day >= self.day_last:
                self.days.append(day)

        if len(self.days) > 0:
            self.days_idx = 0
            
        log.info('Device: %d, raw days: %d, days=%d, day_last=%d, hour_last=%d' % (self.device_id, len(days_raw), len(self.days), self.day_last, self.hour_last))

    def fetch_ts_hours(self):
        self.hours_idx = -1
        self.hours = []
        self.hour = None
        if self.device_id == -1 or self.day == -1:
            return
        
        ts_hours_url = self.base_url + '/devices/%d/timeseries/%d' % (self.device_id, self.day)
        log.info('Init: fetching timeseries hours list from URL: "%s" ...' % ts_hours_url)
        # Set the next "last values" URL for device and increment to next
        json_str = self.read_from_url(ts_hours_url)
        json_obj = self.parse_json_str(json_str)
        hours_all = json_obj['hours']
        for h in hours_all:
            hour = int(h)
            if self.day > self.day_last or (self.day == self.day_last and hour >= self.hour_last):
                self.hours.append(hour)

        if len(self.hours) > 0:
            self.hours_idx = 0
        log.info('%d processable hours for device %d day %d' % (len(self.hours), self.device_id, self.day))

    def next_day(self):
        # All days for current device done? Try next device
        if self.day == -1:
            self.device_id, self.device_ids_idx = self.next_entry(self.device_ids, self.device_ids_idx)

        # If not yet all devices done fetch days current device
        if self.device_id > -1:
            self.fetch_ts_days()
            self.day, self.days_idx = self.next_entry(self.days, self.days_idx)

    def next_hour(self):

        # Pick an hour entry
        self.hour, self.hours_idx = self.next_entry(self.hours, self.hours_idx)

        while self.hour < 0:

            # Pick a next day entry
            self.day, self.days_idx = self.next_entry(self.days, self.days_idx)

            if self.day < 0:
                self.next_day()

            if self.day > -1:
                self.fetch_ts_hours()

            if self.device_id < 0:
                log.info('Processing all devices done')
                break

            # Pick an hour entry
            self.hour, self.hours_idx = self.next_entry(self.hours, self.hours_idx)

    def before_invoke(self, packet):
        """
        Called just before Component invoke.
        """

        # Try to fill in: should point to next hour timeseries REST URL
        self.url = None

        if self.has_expired() or self.all_done():
            # All devices read or timer expiry
            log.info('Processing halted: expired or all done')
            packet.set_end_of_stream()
            return False

        self.next_hour()

        # Still hours?
        if self.hour > 0:
            # The base method read() will fetch self.url until it is set to None
            # <base_url>/devices/14/timeseries/20160603/18
            self.url = self.base_url + '/devices/%d/timeseries/%d/%d' % (self.device_id, self.day, self.hour)
            log.info('self.url = ' + self.url)

        if self.device_id < 0:
            log.info('Processing all devices done')
            return True

        # ASSERT : still device(s) to be done get next hour to process
        return True

    # Create a data record for timeseries of current device/day/hour
    def format_data(self, data):

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
        record['unique_id'] = '%d-%d-%d' % (self.device_id, self.day, self.hour)

        # Timestamp of sample
        record['device_id'] = self.device_id
        record['day'] = self.day
        record['hour'] = self.hour

        # Add JSON text blob
        record['data'] = data

        return record

# -*- coding: utf-8 -*-
#
# MeasurementsDbInput: Reads RIVM raw AQ/LML file data from measurements table and converts to recordlist
#
# Author:Just van den Broecke

from stetl.util import Util, etree
from stetl.inputs.dbinput import PostgresDbInput
from stetl.packet import FORMAT
from stetl.postgis import PostGIS

from datetime import datetime

log = Util.get_log("MeasurementsDbInput")

class MeasurementsDbInput(PostgresDbInput):
    """
    Reads RIVM raw AQ/LML file data from measurements table and converts to recordlist
    """
    def __init__(self, configdict, section):
        PostgresDbInput.__init__(self, configdict, section)
        self.progress_query = self.cfg.get('progress_query')
        self.progress_update = self.cfg.get('progress_update')
        self.db = None

    def after_chain_invoke(self, packet):
        """
        Called right after entire Component Chain invoke.
        Used to update last id of processed file record.
        """
        log.info('Updating progress table with last_id= %d' % self.last_id)
        self.db.execute(self.progress_update % self.last_id)
        self.db.commit(close=False)
        log.info('Update progress table ok')
        return True

    def read(self, packet):

        # Get last processed id of measurementss table
        rowcount = self.db.execute(self.progress_query)
        progress_rec = self.db.cursor.fetchone()
        self.last_id = progress_rec[3]
        log.info('progress record: %s' % str(progress_rec))

        # Fetch next batch of measurementss records
        measurements_recs = self.do_query(self.query % self.last_id)

        log.info('read measurements_recs: %d' % len(measurements_recs))
        # No more records to process?
        if len(measurements_recs) == 0:
            packet.set_end_of_stream()
            log.info('Nothing to do. All file_records done')
            return packet

         # Remember last id processed for next query
        self.last_id = measurements_recs[len(measurements_recs)-1].get('gid')

        packet.data = measurements_recs

        # Always stop after batch, otherwise we would continue forever
        packet.set_end_of_stream()

        return packet
