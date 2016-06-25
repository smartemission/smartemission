# -*- coding: utf-8 -*-
#
# RawSensorDbInput: Reads RIVM raw AQ/LML file data from measurements table and converts to recordlist
#
# Author:Just van den Broecke

from stetl.component import Config
from stetl.packet import FORMAT
from stetl.util import Util
from stetl.inputs.dbinput import PostgresDbInput

log = Util.get_log("RawSensorDbInput")

class RawSensorDbInput(PostgresDbInput):
    """
    Reads raw Smartem json data from timeseries table and converts to recordlist.
    """

    @Config(ptype=str, required=True, default=None)
    def gids_query(self):
        """
        The query (string) to fetch all gid's (id's) to be processed..
        """
        pass

    @Config(ptype=str, required=True, default=None)
    def data_query(self):
        """
        The query (string) to fetch data (json) record for single gid.
        """
        pass

    def __init__(self, configdict, section):
        PostgresDbInput.__init__(self, configdict, section, produces=FORMAT.record)
        self.progress_query = self.cfg.get('progress_query')
        self.db = None

        # Init all timeseries id's
        self.ts_gids = []
        self.ts_gids_idx = 0
        self.ts_gid = -1

    def next_entry(self, a_list, idx):
        if len(a_list) == 0 or idx >= len(a_list):
            idx = -1
            entry = -1
        else:
            entry = a_list[idx]
            idx += 1

        return entry, idx

    def init(self):
        PostgresDbInput.init(self)

        # get gid where to start
        self.last_id = 0

        # One time: get all gid's to be processed
        ts_gid_recs = self.do_query(self.gids_query % self.last_id)

        # Reset columns: we want all columns
        self.column_names = None
        self.columns = None

        log.info('read timeseries_recs: %d' % len(ts_gid_recs))
        for ts_gid_rec in ts_gid_recs:
            self.ts_gids.append(ts_gid_rec['gid'])

        # Pick a first device id
        # self.device_id, self.device_ids_idx = self.next_entry(self.device_ids, self.device_ids_idx)

    def read(self, packet):

        # Get last processed id of measurementss table
        # rowcount = self.db.execute(self.progress_query)
        # progress_rec = self.db.cursor.fetchone()
        # self.last_id = progress_rec[3]
        # log.info('progress record: %s' % str(progress_rec))
        self.ts_gid, self.ts_gids_idx = self.next_entry(self.ts_gids, self.ts_gids_idx)

        # No more records to process?
        if self.ts_gid < 0:
            packet.set_end_of_stream()
            log.info('Nothing to do. All file_records done')
            return packet

        ts_data_rec = self.do_query(self.data_query % self.ts_gid)

        # Remember last id processed for next query     (automatically done via trigger)

        packet.data = ts_data_rec[0]
        log.info('data: %s' % str(packet.data))

        return packet
