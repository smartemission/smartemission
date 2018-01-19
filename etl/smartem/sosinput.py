import json
import re
from datetime import datetime
from stetl.component import Config
from stetl.inputs.httpinput import HttpInput
from stetl.util import Util

log = Util.get_log("SosInput")


# http://inspire.rivm.nl/sos/eaq/api/v1/features/?service=RIVM_inspire&locale=en
# http://inspire.rivm.nl/sos/eaq/api/v1/categories/?service=RIVM_inspire&locale=en&feature=303
# http://inspire.rivm.nl/sos/eaq/api/v1/phenomena/?service=RIVM_inspire&locale=en&feature=303&category=130
# http://inspire.rivm.nl/sos/eaq/api/v1/procedures/?service=RIVM_inspire&locale=en&feature=303&category=130&phenomenon=130
# http://inspire.rivm.nl/sos/eaq/api/v1/timeseries/303/getData?timespan=2016-12-20T22%3A00%3A00%2B01%3A00%2F2016-12-22T01%3A59%3A59%2B01%3A00&

class SosInput(HttpInput):
    """
    Interacts with JSON SOS API

    Algorithm:
        * Get feature info (first timestamp)
        * While features left
            - timestamp = first timestamp feature
            - While timestamp < now
                - Get data from timestamp and feature
                - Increase timestamp (local and db)
        * Switch to next feature
        
    """

    @Config(ptype=list, required=True)
    def features(self):
        """
        The features to harvest from the SOS api

        Required: True
        """
        pass

    @Config(ptype=str, required=True)
    def timeseries_path(self):
        """
        The relative path to the timeseries api. Must contain a %s
        that is replaced by the id.

        Required: True
        """

    @Config(ptype=str, required=True)
    def get_data_path(self):
        """
        The relative path to the getData api. Must contain a (%s, %s, %s) for
        the (id, date, duration in hours).

        Required: True
        """

    @Config(ptype=int, default=24, required=True)
    def request_hours(self):
        """
        The amount of hours to request in a single batch.

        Default: 24

        Required: True
        """

    def __init__(self, configdict, section):
        HttpInput.__init__(self, configdict, section)
        self.base_url = self.url
        self.url = None

        self.feature_idx = 0
        self.next_timestamp = -1
        self.feature_info = dict()

    def init(self):
        for feature in self.features:
            time_series_url = self.base_url + self.timeseries_path % feature
            log.info("Searching info for %s" % time_series_url)

            json_str = self.read_from_url(time_series_url)
            json_obj = self.parse_json_str(json_str)
            if json_obj is not None:
                self.feature_info[feature] = json_obj

    def before_invoke(self, packet):
        self.next_entry()

    def after_invoke(self, packet):
        if not (self.more_features_available() or self.more_data_available()):
            log.info("No more features and data available")
            packet.set_end_of_stream()

        if len(packet.data) is 0:
            log.info("No data for %s" % self.current_date().isoformat())

    def format_data(self, data):
        json_obj = self.parse_json_str(data)["values"]
        log.info("Formatting %d elements of json response" % len(json_obj))

        info = self.current_feature_info()
        feature_id = info['id']
        label = info['label']
        station_name = info['station']['properties']['label']
        # feature_name = info['parameters']['feature']['label']
        phenomenon_name = info['parameters']['phenomenon']['label']

        lon, lat, alt = info['station']['geometry']['coordinates']
        for elem in json_obj:
            elem['id'] = feature_id
            elem['label'] = SosInput.save_name(label)
            elem['station_name'] = SosInput.save_name(station_name)
            elem['phenomenon_name'] = SosInput.save_name(phenomenon_name)
            elem['lat'] = lat
            elem['lon'] = lon
            elem['altitude'] = alt
            elem['datetime'] = datetime.utcfromtimestamp(elem['timestamp'] / 1000)

        return json_obj

    def next_entry(self):
        if self.next_timestamp < 0:
            self.set_first_timestamp()
        else:
            self.next_timestamp += self.request_hours * 60 * 60 * 1000
        if not self.more_data_available() and self.more_features_available():
            self.feature_idx += 1
            self.next_timestamp = -1
            log.info("Switching to next feature %s" % self.current_feature())

        self.url = self.current_url()
        log.info("Next entry is %s" % self.url)

    def more_features_available(self):
        """
        :return: If there are more features after the current one
        """
        return self.feature_idx < len(self.features) - 1

    def more_data_available(self):
        """
        :return: If there is more data for the current feature
        """
        return self.current_date() < datetime.now()

    def current_url(self):
        """
        :return: The url for the current feature and date
        """
        params = (self.current_feature(), self.current_date().isoformat(),
                  self.request_hours)
        return self.base_url + self.get_data_path % params

    def current_feature(self):
        return self.features[self.feature_idx]

    def current_feature_info(self):
        return self.feature_info[self.current_feature()]

    def current_date(self):
        return datetime.fromtimestamp(self.next_timestamp / 1000)

    def set_first_timestamp(self):
        info = self.current_feature_info()
        self.next_timestamp = info["firstValue"]["timestamp"]
        log.info("Next timestamp is %s" % self.current_date().isoformat())

    @staticmethod
    def parse_json_str(raw_str):
        # Parse JSON from data string
        json_obj = None
        try:
            json_obj = json.loads(raw_str)
        except Exception as e:
            log.error('Cannot parse JSON from %s, err= %s' % (raw_str, str(e)))

        return json_obj

    @staticmethod
    def save_name(text):
        return re.subn(r'\W', '_', text)[0].lower().strip()
