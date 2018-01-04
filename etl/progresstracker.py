# -*- coding: utf-8 -*-
#
# Filter to track progress of a stream of processed records in a Postgres table.
#
# Author: Pieter Marsman - 2016
# Adapted by Just van den Broecke 2018

from stetl.component import Config
from stetl.filter import Filter
from stetl.util import Util
from stetl.packet import FORMAT
from stetl.postgis import PostGIS

log = Util.get_log("ProgressTracker")


class ProgressTracker(Filter):
    """"
    Filter to track progress of a stream of processed records.
    Stores progress (last id, last timestamp etc) in Postgres table.
    """

    @Config(ptype=str, required=False, default='localhost')
    def host(self):
        """
        host name or host IP-address, defaults to 'localhost'
        """
        pass

    @Config(ptype=str, required=False, default='5432')
    def port(self):
        """
        port for host, defaults to '5432'
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def user(self):
        """
        User name, defaults to 'postgres'
        """
        pass

    @Config(ptype=str, required=False, default='postgres')
    def password(self):
        """
        User password, defaults to 'postgres'
        """
        pass

    @Config(ptype=str, required=False, default='public')
    def schema(self):
        """
        The postgres schema name, defaults to 'public'
        """
        pass

    @Config(ptype=str, required=False, default='progress')
    def table(self):
        """
        Table name, defaults to 'progress'.
        """
        pass

    @Config(ptype=str, required=True)
    def progress_update_query(self):
        """
        Query to update progress

        Required: True

        Default: ""
        """
        pass

    @Config(ptype=str, required=True)
    def id_key(self):
        """
        Key to select id from record array

        Required: True
        """

    @Config(ptype=str, default=None, required=False)
    def name_key(self):
        """
        Key to select name from record array

        Required: True
        """

    def __init__(self, config_dict, section):
        Filter.__init__(self, config_dict, section,
                        consumes=[FORMAT.record_array, FORMAT.record],
                        produces=[FORMAT.record_array, FORMAT.record])
        self.last_ids = None
        self.db = None
        
    def init(self):
        self.db = PostGIS(self.cfg.get_dict())
        self.db.connect()

    def invoke(self, packet):
        self.last_ids = dict()

        if packet.data is None or packet.is_end_of_doc() or packet.is_end_of_stream():
            log.info("No packet data or end of doc/stream")
            return packet

        record_in = packet.data
        if type(record_in) is not list:
            record_in = [record_in]

        for record in record_in:
            if self.name_key is not None:
                name = record[self.name_key]
            else:
                name = "all"
            if len(record) > 0:
                new = record[self.id_key]
                self.last_ids[name] = max(self.last_ids.get(name, -1), new)

        log.info("Last ids are: %s", str(self.last_ids))

        return packet

    def after_chain_invoke(self, packet):
        """
        Called right after entire Component Chain invoke.
        Used to update last id of processed file record.
        """
        for name in self.last_ids:
            param_tuple = (self.last_ids[name], name)
            log.info('Updating progress table with (id=%d, name=%s)' % param_tuple)
            self.db.execute(self.progress_update_query % param_tuple)
            self.db.commit(close=False)
            log.info('Update progress table ok')
        else:
            log.info('No update for progress table')
        
        return True
