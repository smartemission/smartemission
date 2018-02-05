# -*- coding: utf-8 -*-
#
# RawSensorLastInput: fetch last raw values from CityGIS/Intemo Raw Sensor REST API.
#
# Author:Just van den Broecke

import time
from stetl.component import Config
from stetl.util import Util
from stetl.packet import FORMAT
from stetl.postgis import PostGIS
from smartem.rawsensorapi import RawSensorAPIInput

log = Util.get_log("RawSensorTimeseriesInput")


class RawSensorTimeseriesInput(RawSensorAPIInput):
    """
    Raw Sensor REST API (CityGIS and Intemo servers) TimeSeries (History) fetcher/formatter.

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
    - fetch and store each, starting with the last hour perviously stored
    - ignore timeseries for current day/hour, as the hour will not be yet filled (and Refiner may else already process)
    - stored entry: device_id, day, hour, last_flag, json blob
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

    @Config(ptype=str, default=None, required=True)
    def progress_table(self):
        """
        The Postgres table tracking all last processed days/hours for each device.

        Required: True

        Default: None
        """
        pass

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

        # 2016-10-30 08:12:09,921 RawSensorAPI INFO Device: 55, raw days: 5, days=1, day_last=20161030, hour_last=7
        # 2016-10-30 08:12:09,922 RawSensorAPI INFO Init: fetching timeseries hours list from URL: "http://whale.citygis.nl/sensors/v1/devices/55/timeseries/20161030" ...
        # 2016-10-30 08:12:10,789 RawSensorAPI INFO 1 processable hours for device 55 day 20161030
        # 2016-10-30 08:12:10,789 RawSensorAPI INFO Skipped device-day-hour: 55-20161030-8 (it is still sampling current hour 7)
        # 2016-10-30 08:26:59,172 RawSensorAPI INFO Device: 55, raw days: 5, days=1, day_last=20161030, hour_last=7
        # 2016-10-30 08:26:59,172 RawSensorAPI INFO Init: fetching timeseries hours list from URL: "http://whale.citygis.nl/sensors/v1/devices/55/timeseries/20161030" ...
        # 2016-10-30 08:26:59,807 RawSensorAPI INFO 1 processable hours for device 55 day 20161030
        # 2016-10-30 08:26:59,808 RawSensorAPI INFO self.url = http://whale.citygis.nl/sensors/v1/devices/55/timeseries/20161030/8

        # 2016-10-30 10:37:30,010 RawSensorAPI INFO Init: fetching timeseries days list from URL: "http://whale.citygis.nl/sensors/v1/devices/71/timeseries" ...
        # 2016-10-30 10:37:30,170 RawSensorAPI INFO Device: 71, raw days: 7, days=1, day_last=20161030, hour_last=9
        # 2016-10-30 10:37:30,170 RawSensorAPI INFO Init: fetching timeseries hours list from URL: "http://whale.citygis.nl/sensors/v1/devices/71/timeseries/20161030" ...
        # 2016-10-30 10:37:30,525 RawSensorAPI INFO 1 processable hours for device 71 day 20161030
        # 2016-10-30 10:37:30,525 RawSensorAPI INFO Skipped device-day-hour: 71-20161030-10 (it is still sampling current hour 9)
        # 2016-10-30 10:47:17,095 RawSensorAPI INFO Device: 71, raw days: 7, days=1, day_last=20161030, hour_last=9
        # 2016-10-30 10:47:17,095 RawSensorAPI INFO Init: fetching timeseries hours list from URL: "http://whale.citygis.nl/sensors/v1/devices/71/timeseries/20161030" ...
        # 2016-10-30 10:47:17,511 RawSensorAPI INFO 1 processable hours for device 71 day 20161030
        # 2016-10-30 10:47:17,511 RawSensorAPI INFO self.url = http://whale.citygis.nl/sensors/v1/devices/71/timeseries/20161030/10
        # 2016-10-30 10:57:12,325 RawSensorAPI INFO Init: fetching timeseries days list from URL: "http://whale.citygis.nl/sensors/v1/devices/71/timeseries" ...
        # 2016-10-30 10:57:12,524 RawSensorAPI INFO Device: 71, raw days: 7, days=1, day_last=20161030, hour_last=10
        # 2016-10-30 10:57:12,524 RawSensorAPI INFO Init: fetching timeseries hours list from URL: "http://whale.citygis.nl/sensors/v1/devices/71/timeseries/20161030" ...
        # 2016-10-30 10:57:12,952 RawSensorAPI INFO 0 processable hours for device 71 day 20161030

        # 2016-10-30 12:29:11,534 RawSensorAPI INFO self.url = http://whale.citygis.nl/sensors/v1/devices/71/timeseries/20161030/11 cur_day=20161030 cur_hour=11
        # 2016-10-30 12:29:13,177 RawSensorAPI INFO Skipped device-day-hour: 71-20161030-12 (it is still sampling current hour 11)

        ts_hours_url = self.base_url + '/devices/%d/timeseries/%d' % (self.device_id, self.day)
        log.info('Init: fetching timeseries hours list from URL: "%s" ...' % ts_hours_url)
        # Set the next "last values" URL for device and increment to next
        json_str = self.read_from_url(ts_hours_url)
        json_obj = self.parse_json_str(json_str)
        hours_all = json_obj['hours']

        # Get the current day and hour in UTC
        current_day, current_hour = self.get_current_day_hour()
        for h in hours_all:
            hour = int(h)
            if self.day > self.day_last or (self.day == self.day_last and hour > self.hour_last):
                if self.day_last == current_day and hour - 1 >= current_hour:
                    # never append the last hour of today
                    log.info('Skip current hour from %d to %d for device %d on day %d' % (hour, hour, self.device_id, self.day))
                else:
                    self.hours.append(hour)

        if len(self.hours) > 0:
            self.hours_idx = 0
        log.info('processable hours for device %d day %d: %s' % (self.device_id, self.day, str(self.hours)))

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

    def get_current_day_hour(self):
        # Get the current day and hour in UTC
        current_time = time.gmtime()
        current_day = int(time.strftime('%Y%m%d', current_time))
        current_hour = int(time.strftime('%H',current_time))
        return current_day, current_hour

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

        # Get the current day and hour in UTC
        current_day, current_hour = self.get_current_day_hour()

        # Skip harvesting the current hour as it will not yet be complete, so try the next device, hour
        # 2016-10-30 08:12:10,789 RawSensorAPI INFO Skipped device-day-hour: 55-20161030-8 (it is still sampling current hour 7)
        skips = 0
        while self.day == current_day and (self.hour - 1) == current_hour and not self.all_done():
            skips += 1
            log.info('Skip #%d: device-day-hour: %d-%d-%d (still sampling current hour %d)' % (skips, self.device_id, self.day, self.hour, current_hour))
            # Force to skip to next device, sometimes we have an even later hour
            self.next_hour()
            # 30.okt.16: Fix for #24 #25 gaps in data: because next_hour() may jump to next device and unconditionally fetch current hour...
            # so fix is to use while loop until a valid hour available or we are all done
            # 5.2.18 : tried incomplete hours as complete = False but this 

        # Still hours?
        if self.hour > 0:
            # The base method read() will fetch self.url until it is set to None
            # <base_url>/devices/14/timeseries/20160603/18
            self.url = self.base_url + '/devices/%d/timeseries/%d/%d' % (self.device_id, self.day, self.hour)
            log.info('self.url = %s cur_day=%d cur_hour=%d' % (self.url, current_day, current_hour))

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
        #   unique_id character varying not null,
        #   insert_time timestamp with time zone default current_timestamp,
        #   device_id integer not null,
        #   day integer not null,
        #   hour integer not null,
        #   data json,
        #   complete boolean default false,
        #   device_type character varying not null default 'jose',
        #   device_version character varying not null default '1',
        #   PRIMARY KEY (gid)
        # ) WITHOUT OIDS;


        # Create record with JSON text blob with metadata
        record = dict()
        record['unique_id'] = '%d-%d-%d' % (self.device_id, self.day, self.hour)

        # Timestamp of sample
        record['device_id'] = self.device_id
        record['day'] = self.day
        record['hour'] = self.hour

        # Assume hour is "complete" (5.2.18: skip complete = False entries for now).
        record['complete'] = True
        # cur_day, cur_hour = self.get_current_day_hour()
        # if cur_day > record['day'] \
        #         or (cur_day == record['day'] and cur_hour >= record['hour']):
        #     record['complete'] = True

        # Add JSON text blob
        record['data'] = data

        return record
