# -*- coding: utf-8 -*-
#
# Smart Emission DB input classes.
#
# Author: Just van den Broecke

from stetl.component import Config
from stetl.util import Util
from stetl.inputs.dbinput import PostgresDbInput

log = Util.get_log("SmartemDbInput")


class RefinedDbInput(PostgresDbInput):
    """
    Reads SmartEmission refined timeseries data from table and converts to recordlist.
    """

    @Config(ptype=int, required=True, default=10)
    def max_input_records(self):
        """
        Maximum number of input (refined) records to be processed.
        """
        pass

    def __init__(self, configdict, section):
        PostgresDbInput.__init__(self, configdict, section)
        self.progress_query = self.cfg.get('progress_query')
        self.progress_update = self.cfg.get('progress_update')
        self.db = None
        self.last_id = None

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

        # Get last processed id of measurements table
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

        # Stop if read_once is set, otherwise read until len(measurements_recs) is 0
        if self.read_once:
            packet.set_end_of_stream()

        return packet
