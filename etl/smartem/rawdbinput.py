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

        # NB the last_gis is automatically set via TRIGGER
        # in the PostgresDB output
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

        self.read_gids()
        self.read_records()

    def read_gids(self):

        # get gid where to start
        last_gid_tuples = self.raw_query(self.last_gid_query)
        if len(last_gid_tuples) == 1:
            self.last_gid, = last_gid_tuples[0]

    def read_records(self):

        # One time: get all gid's to be processed
        raw_query = self.gids_query % (self.last_gid, self.last_gid + self.max_input_records)
        ts_gid_tuples = self.raw_query(raw_query)
        ts_gid_recs = self.tuples_to_records(ts_gid_tuples, ['gid'])

        log.info('read timeseries_recs: %d' % len(ts_gid_recs))
        self.ts_gids = []
        for rec in ts_gid_recs:
            self.ts_gids.append(rec['gid'])

    def read(self, packet):

        # Next entry from ts record list
        self.ts_gid, self.ts_gids_idx = self.next_entry(self.ts_gids, self.ts_gids_idx)

        # No more records to process?
        if self.ts_gid < 0:
            if self.read_once:
                # One round: we're done
                packet.set_end_of_stream()
                log.info('Nothing to do. All file_records done')
                return packet
            else:
                # Continue fetching recs from from last_gid
                self.last_gid += self.max_input_records
                self.read_records()
                self.ts_gids_idx = 0
                if len(self.ts_gids) > 0:
                    self.ts_gid, self.ts_gids_idx = self.next_entry(self.ts_gids, self.ts_gids_idx)
                    log.info('Continuing from gid=%d' % self.ts_gid)
                else:
                    packet.set_end_of_stream()
                    log.info('Nothing to do. read_once=False, All file_records done')
                    return packet

        packet.data = self.do_query(self.data_query % self.ts_gid)
        # log.info('data: %s' % str(packet.data))

        return packet
