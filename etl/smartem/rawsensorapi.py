# -*- coding: utf-8 -*-
#
# RawSensorInput: fetch raw values from CityGIS Raw Sensor REST API.
#
# Author:Just van den Broecke

import json
import time
import random
from stetl.component import Config
from stetl.util import Util
from stetl.inputs.httpinput import HttpInput
from stetl.packet import FORMAT

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

    @Config(ptype=list, default=[], required=False)
    def skip_devices(self):
        """
        List of strings with device id's that need to be skipped.

        Required: False

        Default: None
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
            device_id = d.split('/')[-1]

            # Skip id's of e.g. obsolete or transfered devices
            if device_id in self.skip_devices:
                continue

            self.device_ids.append(int(device_id))

        if len(self.device_ids) > 0:
            self.device_ids_idx = 0
            # For bether throughput as WHale server is too slow
            # If we do sequentially higher dev numbers would not be processed.
            random.shuffle(self.device_ids)
            # self.device_ids = [20010004]

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
        except Exception as e:
            log.error('Cannot parse JSON from %s, err= %s' % (raw_str, str(e)))
            raise e

        return json_obj
