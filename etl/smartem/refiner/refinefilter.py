# -*- coding: utf-8 -*-
#
# Filter to consume a raw record of Smart Emission data (one hour for one device) ,
# refining these, producing records by calling a Refiner specific to device type.
#


# Author: Just van den Broecke - 2015-2018

from stetl.filter import Filter
from stetl.util import Util
from stetl.packet import FORMAT
from stetl.component import Config

from refiner import Refiner

log = Util.get_log("RefineFilter")


class RefineFilter(Filter):
    """
    Filter to consume single raw record with sensor (single hour) timeseries values and produce refined record for each component.
    Refinement entails: calibration (e.g. Ohm to ug/m3) and aggregation (hour-values).
    Input is a single timeseries record for a single hour with all sensorvalues for a single device within that hour.
    """

    @Config(ptype=list, default=[], required=True)
    def sensor_names(self):
        """
        The output sensor names to refine.

        Required: True

        Default: []
        """
        pass

    @Config(ptype=str, default='refiner', required=True)
    def process_name(self):
        """
        The process name (for calibration).

        Required: True

        Default: refiner
        """
        pass

    def __init__(self, configdict, section):
        Filter.__init__(self, configdict, section, consumes=FORMAT.record, produces=FORMAT.record_array)
        self.refiners = dict()

    def get_refiner(self, record):
        """
        Find a Refiner specific to device type (Josene, AirSensEUR etc)
        :param refiner:
        :return:
        """

        if 'device_type' not in record:
            log.warn('No device_type attr in record=%s' % record['device_id'] )
            return None

        device_type = record['device_type']
        if device_type not in self.refiners:
            refiner = Refiner.get_refiner(device_type)

            # One-time init of Refiner (may init calibration setup)
            refiner.init(self.cfg.config_dict)
            self.refiners[device_type] = refiner

        return self.refiners[device_type]

    def exit(self):
        for device_type in self.refiners:
            # One-time exit of Refiner (may save calibration state)
            self.refiners[device_type].exit()

    def invoke(self, packet):

        if packet.data is None or \
                packet.is_end_of_doc() or \
                packet.is_end_of_stream():
            return packet

        refiner = self.get_refiner(packet.data)
        if not refiner:
            packet.data = None
            return packet

        # Let the Refiner specific to device type do all refinement steps
        # returning an array of records.
        packet.data = refiner.refine(packet.data, self.sensor_names)

        return packet
