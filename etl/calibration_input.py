import pickle
from stetl.component import Config
from stetl.inputs.dbinput import PostgresDbInput
from stetl.inputs.fileinput import FileInput
from stetl.packet import FORMAT
from stetl.util import Util

import pandas as pd

log = Util.get_log('Calibration input')


class CalibrationDataInput(FileInput):
    def __init__(self, configdict, section, produces=FORMAT.record):
        FileInput.__init__(self, configdict, section, produces)

    def read_file(self, file_path):
        log.debug("Reading data from file")
        df = pd.DataFrame.from_csv(file_path)
        return {'merged': df}


class CalibrationModelInput(PostgresDbInput):
    """
    Get unpickled calibration model from the database
    """

    @Config(ptype=dict, default=dict(), required=False)
    def sensor_model_names(self):
        """
        The name of the sensor models in the database. Needed for linking
        the right model to the right gas.

        Default: dict()

        Required: False
        """

    def __init__(self, configdict, section):
        PostgresDbInput.__init__(self, configdict, section)
        self.models = None

    def init(self):
        PostgresDbInput.init(self)

        def get_model(name):
            query = self.query % name
            log.info('Getting calibration model with query: %s' % query)
            ret = self.raw_query(query)
            if len(ret) > 0:
                return pickle.loads(str(ret[0][0]))
            else:
                log.warn("No model found for %s" % name)
                return None

        if self.query is not None and len(self.sensor_model_names) > 0:
            log.info('Getting calibration models from database')
            self.models = {k: get_model(v) for k, v in
                           self.sensor_model_names.iteritems()}
        else:
            log.info('No query for fetching calibration models given or no '
                     'mapping for calibration models to gas components given.')

    def invoke(self, packet):
        packet.meta['models'] = self.models

        return packet
