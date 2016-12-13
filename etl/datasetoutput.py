# -*- coding: utf-8 -*-
#
# Save packets to disk
#
# Author: Pieter Marsman - 2016

from stetl.outputs.fileoutput import FileOutput
from stetl.util import Util

from pandas import DataFrame

log = Util.get_log('FileOutputAppend')


class CsvFileOutput(FileOutput):
    def write_file(self, packet, file_path):
        log.info('writing to file %s' % file_path)

        df = DataFrame.from_records(packet.data)
        df.to_csv(file_path, index=False)

        return packet
