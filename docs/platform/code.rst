API and Code
============

Below is the API documention for the SE Platform Python code.

ETL Processes
-------------

Python classes involved in ETL.
Code and config for all ETL can be found in the `SE GitHub <https://github.com/Geonovum/smartemission/tree/master/etl>`_.

Harvesting from Whale
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: rawsensorapi
   :members:

SE PostGIS DB
~~~~~~~~~~~~~

.. automodule:: smartemdb
   :members:


Calibration and Refinement
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: extractor
   :members:

.. automodule:: calibration
   :members:


.. automodule:: refiner
   :members:

.. automodule:: sensorconverters
   :members:

.. automodule:: sensordefs
   :members:

InfluxDB
~~~~~~~~

.. automodule:: influxdbinput
   :members:

.. automodule:: influxdboutput
   :members:

SOS Input/Output
~~~~~~~~~~~~~~~~

.. automodule:: sosinput
   :members:

.. automodule:: sosoutput
   :members:

SensorThings API
~~~~~~~~~~~~~~~~

.. automodule:: staoutput
   :members:
