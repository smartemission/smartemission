.. _sensors:

=======
Sensors
=======

Originally the SE Platform was developed for a single sensor device (station), the Intemo Jose(ne).
As time moved on additional sensor devices from various sensor projects were integrated,
or are in progress. To allow for multiple sensor stations/devices, each with multiple
internal sensors from multiple projects, internals for mainly the ETL processes (cron jobs) were generalized while still keeping the
core principles of the overall architecture
and multi-step ETL processing: raw data harvesting (pull), refinement (validation, calibration), service-publication.

Based on device/sensor-types different ETL algorithms
need to be applied. For example, some devices already emit calibrated sensor-values (Luftdaten, Osiris), others require ANN calibration (Jose), others
even per-sensor linear or polynominal equations, sometimes per-sensor (AirSensEUR AlphaSense).

The advantage of the current approach is that once measurements are 'in', they
become automatically available through all external APIs without any additional action. Only on the 'input' (harvesting)-side
and refinement ETL are specific formatting steps required.

Principles
==========

To integrate a new sensor station type, two main items need to be resolved:

* APIs from which sensor-data can be harvested ('getting the raw or sometimes calibrated data in')
* amount/complexity of calibration and validation needed

In addition, a sensor station type is usually related to a Project. In an early stage
every device was given a unique id, where the first 4 digits is the project id, followed by additional
digits, denoting the station id within that project. Sometimes a mapping is required.
The original station id is always kept in metadata columns.

APIs
----

Data from sensors is never sent directly to the SE platform.
It is sent to what are called **Data Collectors**. These are usually not maintained by SE but
by the specific projects like *Smart City Living Lab*, *Luftdaten* and/or companies like *Intemo* etc.
The only requirement is that these
Data Collectors provide APIs for pulling data into (Harvesting) the SE Platform.

Currently, harvesting from three Data Collector APIs has been realized:

1. Raw Sensor (a.k.a. Whale) API from now mainly Intemo (Jose stations) servers

2. InfluxDB Data Collector API, now mainly for `AirSensEUR <https://airsenseur.org>`_ stations

3. `Luftdaten API <https://github.com/opendata-stuttgart/meta/wiki/APIs>`_, for `Luftdaten.info <https://luftdaten.info/en/home-en/>`_ kits

Ad 2) this InfluxDB API is maintained by the SE Project itself and may be used in later projects to publish (push) data from additional sensors.


Calibration
-----------

Currently, the following calibration algorithms are implemented:

1. Jose stations: ANN Calibration

2. `AirSensEUR <https://airsenseur.org>`_ per-sensor linear or polynominal equations

3. `Luftdaten.info <https://luftdaten.info/en/home-en/>`_ : no calibration required

These algorithms are reusable, mainly the parameters for each need to be set.

So how is this realized internally? Basic principles:

* while harvesting as much metadata as possible is extracted or configured
* the programming concept of an abstract `Device <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/device.py>`_ and `Device registry <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/devicereg.py>`_

Each station-type (Jose, ASE, Luftdaten) is mapped to a Device Type. From there, specific processing, configuration and
algorithms are invoked. A special Device Type is the `Vanilla Device <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/vanilla.py>`_.
The Vanilla Device Type can be used when no specific calibration is required. This is the easiest way to attach stations
and was introduced when attaching kits from the `Luftdaten Project <https://luftdaten.info/en/home-en/>`_ .

Each Device has one to three additional items/files:

* Device Definitions ("device devs"), these map component indicators like `no2`, `temperature` etc to their raw inputs and provides pointers to the functions that perform converting (e.g. via calibration) the raw inputs, plus min/max values for validation
* Device Functions: functions that provide all conversions/calibrations
* Device Params (AirSensEUR-AlphaSense sensors only): per-device calibration params

The Refiner mainly invokes these as abstract items without specific knowledge of the Device or sensor type.

Examples:

1) Jose Stations:

* `Device <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/josene.py>`_
* `Device Definitions <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/josenedefs.py>`_
* `Device Functions <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/josenefuncs.py>`_   (invoke ANN)

2) AirSensEUR Stations:

* `Device <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/airsenseur.py>`_
* `Device Definitions <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/airsenseurdefs.py>`_
* `Device Functions <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/airsenseurfuncs.py>`_
* `Per-sensor params <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/airsenseurparms.py>`_  (provided by M. Gerboles, EU JRC)

3) Luftdaten Kits (using Vanilla Device):

* `Vanilla Device <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/vanilla.py>`_
* `Vanilla Device Definitions <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/vanilladefs.py>`_  generic defs, no specific implementation required


Additional Info
===============

Some specifics per station type and projects.

Luftdaten Kits
--------------

With the introduction of the  `Vanilla Device <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/devices/vanilla.py>`_ only specific
Harvesting classes needed to be developed:

* Last Values harvesting - using the "last 5 minute values" API
* General harvesting - using the "last hour average values" API

As to not strain the Luftdaten server intrastructure and to start lightly, only data in specified Bounding Boxes
within the ETL Stetl config, is harvested. In first instance the area of Nijmegen, `[51.7,5.6,51.9,6.0]`, but this can be extended later.

Only three classes are required integrating Luftdaten measurements, the first is a common base-class for all:

* `LuftdatenInput <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/harvester/luftdateninput.py>`_ - a generic Stetl HttpInput-derived class
* `HarvesterLastLuftdatenInput <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/harvester/harvestlastluftdaten.py>`_ - Harvester for last values (near real-time values)
* `HarvesterLuftdatenInput <https://github.com/smartemission/docker-se-stetl/blob/master/smartem/harvester/harvestluftdaten.py>`_ - Harvester for last-hour average values (history timeseries)

These classes mainly process incoming JSON-data to required database record formats for generic Stetl `PostgresInsert` output classes.

The Stetl configurations as run in the ETL cronjobs are:

* `Last Values Stetl Config <https://github.com/smartemission/docker-se-stetl/blob/master/config/last.cfg>`_ - Common Harvester for all last values (near real-time values)
* `Harvester Stetl Config <https://github.com/smartemission/docker-se-stetl/blob/master/config/harvester_luftdaten.cfg>`_ - Harvester for last-hour average values (history timeseries)

Device id's consist of a fixed `project id`, `4931` (German and Dutch country codes) followed by 4-5 digits Luftdaten `Location id`. Although
each LTD sensor has its own unique id, the Location Id (and related lat/lon) binds multiple sensors together and can be considered as a "kit" or "station".

No specific code is required for any of the other SE ETL processes, like Refiner and SOS and STA Publishers. For example all Luftdaten STA `Things` can be queried
by the project id `4931`: https://data.smartemission.nl/gost/v1.0/Things?$filter=properties/project_id%20eq%20%274931%27


AirSensEUR
----------

To Be Supplied.

Project id is `1182`.

Via STA:
https://data.smartemission.nl/gost/v1.0/Things?$filter=properties/project_id%20eq%20%271182%27

Josene
------

To Be Supplied.

Several projects including Smart City Living Lab, Waalkade. The original Nijmegen SE project has project id '0000', others usually start with '2'.

