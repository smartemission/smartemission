# -*- coding: utf-8 -*-
#
# Smart Emission DB input classes.
#
# Author: Just van den Broecke

from stetl.component import Config
from stetl.util import Util
from stetl.inputs.dbinput import PostgresDbInput

log = Util.get_log("SmartemDbInput")

class RawDbInput(PostgresDbInput):
    """
    Reads raw Smartem Harvested json data from timeseries table and converts to recordlist.
    """

    @Config(ptype=str, required=True, default=None)
    def last_gid_query(self):
        """
        The query (string) to fetch last gid that was processed.
        """
        pass

    @Config(ptype=str, required=True, default=None)
    def gids_query(self):
        """
        The query (string) to fetch all gid's (id's) to be processed.
        """
        pass

    @Config(ptype=int, required=True, default=10)
    def max_input_records(self):
        """
        Maximum number of input (raw) records to be processed.
        """
        pass

    @Config(ptype=str, required=True, default=None)
    def data_query(self):
        """
        The query (string) to fetch data (json) record for single gid.
        """
        pass

    def __init__(self, configdict, section):
        PostgresDbInput.__init__(self, configdict, section)
        self.progress_query = self.cfg.get('progress_query')
        self.db = None

        # Init all timeseries id's
        self.ts_gids = []
        self.ts_gids_idx = 0
        self.ts_gid = -1
        self.last_gid = 0

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
        last_gid_tuples = self.raw_query(self.last_gid_query)
        if len(last_gid_tuples) == 1:
            self.last_gid, = last_gid_tuples[0]

        # One time: get all gid's to be processed
        raw_query = self.gids_query % (self.last_gid, self.last_gid + self.max_input_records)
        ts_gid_tuples = self.raw_query(raw_query)
        ts_gid_recs = self.tuples_to_records(ts_gid_tuples, ['gid'])

        log.info('read timeseries_recs: %d' % len(ts_gid_recs))
        for rec in ts_gid_recs:
            self.ts_gids.append(rec['gid'])

        # Pick a first device id
        # self.device_id, self.device_ids_idx = self.next_entry(self.device_ids, self.device_ids_idx)

    def read(self, packet):

        # Get last processed id of measurementss table
        # rowcount = self.db.execute(self.progress_query)
        # progress_rec = self.db.cursor.fetchone()
        # self.last_gid = progress_rec[3]
        # log.info('progress record: %s' % str(progress_rec))
        self.ts_gid, self.ts_gids_idx = self.next_entry(self.ts_gids, self.ts_gids_idx)

        # No more records to process?
        if self.ts_gid < 0:
            packet.set_end_of_stream()
            log.info('Nothing to do. All file_records done')
            return packet

        ts_data_rec = self.do_query(self.data_query % self.ts_gid)

        # Remember last id processed for next query     (automatically done via trigger)

        packet.data = ts_data_rec
        # log.info('data: %s' % str(packet.data))

        return packet


class RefinedDbInput(PostgresDbInput):
    @Config(ptype=int, required=True, default=10)
    def max_input_records(self):
        """
        Maximum number of input (refined) records to be processed.
        """
        pass

    """
    Reads SmartEmission refined timeseries data from table and converts to recordlist.
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

        # Fetch next batch of refined input records
        measurements_recs = self.do_query(self.query % (self.last_id, self.last_id + self.max_input_records))

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
