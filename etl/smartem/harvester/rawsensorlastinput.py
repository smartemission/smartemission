# -*- coding: utf-8 -*-
#
# RawSensorLastInput: fetch last raw values from CityGIS/Intemo Raw Sensor REST API.
#
# Author:Just van den Broecke

import time
from datetime import datetime, timedelta
from stetl.component import Config
from stetl.util import Util
from stetl.packet import FORMAT
from smartem.util.utc import zulu_to_gmt
from smartem.rawsensorapi import RawSensorAPIInput

log = Util.get_log("RawSensorAPI")


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

    def __init__(self, configdict, section, produces=FORMAT.record):
        RawSensorAPIInput.__init__(self, configdict, section, produces)
        self.models = None


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
            # needs to continue such that further in the stream final actions
            # can be taken when stream is ending.
            # i.e. save calibration state at end of stream
            return True

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
        if 'id' not in sensor_vals:
            return None

        if 'p_unitserialnumber' not in sensor_vals:
            sensor_vals['p_unitserialnumber'] = sensor_vals['id']

        record = dict()
        # Timestamp of sample
        record['device_id'] = self.device_id
        record['device_name'] = 'station %d' % self.device_id

        # Determine if hour is "complete"
        record['complete'] = True
        record['last'] = True

        record['device_type'] = 'jose'
        record['device_version'] = '1'

        # Add JSON text blob
        record['data'] = {
            'timeseries': [sensor_vals]
        }

        # Unix timestamp to calculate "stale state (0/1)" i.e. if a station has been
        # active over the last N hours (now 2). We keep all last values but flag inactive stations.
        record['time'] = zulu_to_gmt(sensor_vals['time'])
        utc_then = datetime.utcnow() - timedelta(hours=2)
        tstamp_sample = time.mktime(record['time'].timetuple())
        tstamp_then = time.mktime(utc_then.timetuple())
        record['value_stale'] = 0
        if tstamp_sample < tstamp_then:
            record['value_stale'] = 1

        return record
