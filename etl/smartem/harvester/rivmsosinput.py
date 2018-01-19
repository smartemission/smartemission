from stetl.component import Config
from stetl.inputs.dbinput import PostgresDbInput
from stetl.util import Util
from smartem.sosinput import SosInput

log = Util.get_log("RIVMSosInput")


class RIVMSosInput(SosInput, PostgresDbInput):
    """
    Specialized SOS Input for RIVM SOS, adds progress tracking.
    """

    @Config(ptype=str, required=True)
    def progress_query(self):
        """
        Query to fetch progress for feature

        Required: True
        """

    def __init__(self, configdict, section):
        SosInput.__init__(self, configdict, section)
        PostgresDbInput.__init__(self, configdict, section)
        self.progress = dict()

    def init(self):
        SosInput.init(self)
        PostgresDbInput.init(self)

        progress_list = self.do_query(self.progress_query)
        for progress_row in progress_list:
            name = progress_row["name"]
            timestamp = progress_row["timestamp"]
            self.progress[name] = timestamp

    def set_first_timestamp(self):
        info = self.current_feature_info()

        # if there is already progress for label
        if info["label"] in self.progress:
            self.next_timestamp = self.progress[info["label"]]
            log.info("Using progress table to initialize first timestamp "
                     "for %s" % self.current_feature())
        # if there is no progress for label
        else:
            self.next_timestamp = info["firstValue"]["timestamp"]
            log.info("Using RIVM SOS to initialize first timestamp "
                     "for %s" % self.current_feature())

        log.info("Next timestamp is %s" % self.current_date().isoformat())

    def format_data(self, data):
        json_obj = SosInput.format_data(self, data)

        for elem in json_obj:
            # Station name consist of location and component. Strip of
            # component. Yes, this is a hack to get proper names ;)
            text = elem['station_name']
            text = '__'.join(text.split('__')[:-1])
            elem['station_name'] = text

        return json_obj
