.. _data:

===============
Data Management
===============

This chapter describes all technical aspects related to data/ETL within
the Smart Emission Data Platform
based on the (ETL-)design described within the :ref:`architecture` chapter.

As sensor data is continuously generated, also the ETL processing
is continuous.

As indicated there are three ETL-steps in sequence:

* Harvester - fetch raw sensor values from "Whale server"
* Refiner - validate, convert, calibrate and aggregate raw sensor values
* Publisher - publish refined values to various (OGC) services

The ``Extractor`` is used for Calibration purposes: to publish raw indicators
from the sensors into an ``InfluxDB`` time-series DB.

Implementation for all ETL can be found here:
https://github.com/Geonovum/smartemission/blob/master/etl

General
=======

This section describes general aspects applicable to all ETL processing.

Stetl Framework
---------------

The `ETL-framework Stetl <http://stetl.org>`_ is used for all ETL-steps.
The Stetl framework is general-purpose and written in Python. A specific ETL-process
is constructed by a Stetl config file. This config file specifies
the Inputs, Filters and Outputs and parameters for that ETL-process. Stetl provides a
multitude of reusable Inputs, Filters and Outputs. For example
ready-to-use Outputs for Postgres and HTTP. For specific processing
specific Inputs, Filters and Outputs can be developed by deriving from
Stetl-base classes. This applies
also to the SE-project.

For each ETL-step a specific Stetl config file is developed with
some SE-specific Components.

Deployment of Stetl processes is effected using
a generic `Stetl Docker Image <https://github.com/Geonovum/smartemission/blob/master/docker/stetl>`_
is reused in every ETL-step.

ETL Scheduling
--------------

The three ETL steps are running as scheduled processes using Unix `cron` activated with the
`SE Platform cronfile <https://github.com/Geonovum/smartemission/blob/master/platform/cronfile.txt>`_.

Sync-tracking
-------------

Any continuous ETL, in particular in combination with data from remote systems, is liable to a multitude of
failures: a remote server may be down, systems may be upgraded or restarted, the
ETL software itself may be upgraded. Somehow an ETL-component needs to "keep track"
of its last successful data processing: specifically for which device, which sensor and
which timestamp. As programmatic tracking may suffer those same vulnerabilities, it
was chosen to use the PostgreSQL database for tracking. Each of the three main steps
will track its synchronization within a Postgres table. In the cases of the Harvester
and the Refiner this synchronization is even strongly coupled to a PG `TRIGGER`: i.e.
only if data has been successfully written/committed to the DB will the
sync-state be updated. An ETL-process will always resume at the point of the
last saved sync-state.


Why Multistep?
--------------

Although all ETL could be performed within a single, continuous process, there are several
reasons why a multistep, scheduled ETL processing from all Harvested data
has been beneficial. This in combination with "sync-tracking" provides
the following benefits:

* clear separation of concerns: Harvesting, Refining, Publishing
* all or individual ETL-steps can be "replayed" whenever some bug/enhancement appeared during development
* being more lean towards server downtime and network failures

Each of the three ETL-steps are expanded below.

Harvester
=========

The ``Harvester`` as its name implies, regularly fetches raw sensor data from
the remote raw sensor data-collector, a.k.a. the "CityGIS Whale Server".
The Harvester uses the ``Raw Sensor API`` web-service that was specifically
developed for the project. Via this API timeseries data is fetched as JSON
for each station (device). Each JSON data element contains the
raw data for all sensors within a single station as accumulated in the current or previous
hour. These JSON data blobs are stored by the Harvester within a Postgres DB unmodified.
In this fashion we always will have access to the original raw data.

The Harvester, like all other ETL is developed using the `Stetl ETL framework <http://stetl.org>`_.
As Stetl already supplies a Postgres/PostGIS output, only a specific
reader for the Raw Sensor API needed to be developed:
the `RawSensorTimeseriesInput <https://github.com/Geonovum/smartemission/blob/master/etl/rawsensorapi.py>`_.

Like indicated, the Harvester will regularly fetch data, as scheduled by the
system's crontab

Database
--------

The main table where the Harvester stores its data. Note the use of the ``data`` field
as ``json`` column. The ``device_id`` is the unique station id. ::

	CREATE TABLE smartem_raw.timeseries (
	  gid serial,
	  unique_id character varying (16) not null,
	  insert_time timestamp with time zone default current_timestamp,
	  device_id integer not null,
	  day integer not null,
	  hour integer not null,
	  data json,
	  complete boolean default false,
	  PRIMARY KEY (gid)
	) WITHOUT OIDS;

Implementation
--------------

Below are links to the various implementation files related to the ``Harvester``.

* Shell script: https://github.com/Geonovum/smartemission/blob/master/etl/harvester.sh
* Stetl config: https://github.com/Geonovum/smartemission/blob/master/etl/harvester.cfg
* Stetl input: https://github.com/Geonovum/smartemission/blob/master/etl/rawsensorapi.py
* Database: https://github.com/Geonovum/smartemission/blob/master/etl/db/db-schema-raw.sql

Last Values
-----------

The "Last" values ETL is an optimization/shorthand to provide all three ETL-steps
(Harvest, Refine, Publish) for only the last/current
sensor values within a single ETL process. All refined data is stored within a single
DB-table. This table maintains only last values, no history, thus data is overwritten
constantly. ``value_stale`` denotes when an indicator has not provided a fresh values in
2 hours. ::

	CREATE TABLE smartem_rt.last_device_output (
	  gid serial,
	  unique_id character varying,
	  insert_time timestamp with time zone default current_timestamp,
	  device_id integer,
	  device_name character varying (32),
	  name character varying,
	  label character varying,
	  unit  character varying,
	  time timestamp with time zone,
	  value_raw integer,
	  value_stale integer,
	  value real,
	  altitude integer default 0,
	  point geometry(Point,4326),
	  PRIMARY KEY (gid)
	) WITHOUT OIDS;

Via Postgres VIEWs, the last values for each indicator are extracted, e.g. for the
purpose of providing a per-indicator WMS/WFS layer. For example: ::

	CREATE VIEW smartem_rt.v_last_measurements_NO2_raw AS
	  SELECT device_id, device_name, label, unit,
	    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
	  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no2raw'
	                                                ORDER BY device_id, gid DESC;


In addition, this last-value data from the `last_device_output` table
is unlocked using a subsetted web-service based on the
52North SOS-REST API.

Implementation file for the ``Last Values ETL``:

* https://github.com/Geonovum/smartemission/blob/master/etl/last.sh
* https://github.com/Geonovum/smartemission/blob/master/etl/last.cfg
* https://github.com/Geonovum/smartemission/blob/master/etl/rawsensorapi.py
* database: https://github.com/Geonovum/smartemission/blob/master/etl/db/db-schema-last.sql

NB theoretically last values could be obtained by setting VIEWs on the Refined
data tables and the SOS. However in previous projects this rendered significant
performance implications. Also the Last Values API was historically developed
first before refined history data and SOS were available in the project.

Refiner
=======

Most raw sensor values as harvested from the CityGIS-platform via the Raw Sensor API
need to be converted
and calibrated to standardized units and values. Also values may
be out of range. The sensors themselves will produce an excess data typically every
few seconds while for many indicators (gasses, meteo) conditions will not change
significantly within seconds. Also to make data manageable in all subsequent publication
steps (SOS, WMS etc) a form of ``aggregation`` is required.gr

The `Refiner` implements five data-processing steps:

* Validation (pre)
* Calibration
* Conversion
* Aggregation
* Validation (post)

Validation deals with removing ``outliers``, values outside specific intervals.
Calibration and Conversion go hand-in-hand: in many cases, like Temperature,
the sensor-values are already calibrated but provided in another unit like milliKelvin.
Here a straightforward conversion applies. In particularly raw
gasvalues may come in resistance
values (kOhm). There is no linear relationship with these resistance-values
and standard gas concentration units like mg/m3 or ppm.
In that case Calibration needs to be applied.

Calibration
-----------

Especially for gas-components this may be a challenge. Here raw sensor-values are expressed in
kOhms (NO2, O3 and CO) except for CO2 which is given in ppb. Audio-values are already provided in decibels.
Meteo-values are more standard and obvious to convert (e.g. milliKelvin to deegree Celsius).

The complexity for the calibration of gasses lies in the fact that many parameters may influence
measured values: temperature, relative humidity, pressure and even the concentration of
other gasses! For example O3 and NO2. A great deal of scientific literature is already devoted
to the sensor calibration issue.

The units are: ::

	S.TemperatureUnit		milliKelvin
	S.TemperatureAmbient	milliKelvin
	S.Humidity				%mRH
	S.LightsensorTop		Lux
	S.LightsensorBottom		Lux
	S.Barometer				Pascal
	S.Altimeter				Meter
	S.CO					ppb
	S.NO2					ppb
	S.AcceleroX				2 ~ +2G (0x200 = midscale)
	S.AcceleroY				2 ~ +2G (0x200 = midscale)
	S.AcceleroZ				2 ~ +2G (0x200 = midscale)
	S.LightsensorRed		Lux
	S.LightsensorGreen		Lux
	S.LightsensorBlue		Lux
	S.RGBColor				8 bit R, 8 bit G, 8 bit B
	S.BottomSwitches		?
	S.O3					ppb
	S.CO2					ppb
	v3: S.ExternalTemp		milliKelvin
	v3: S.COResistance		Ohm
	v3: S.No2Resistance		Ohm
	v3: S.O3Resistance		Ohm
	S.AudioMinus5			Octave -5 in dB(A)
	S.AudioMinus4			Octave -4 in dB(A)
	S.AudioMinus3			Octave -3 in dB(A)
	S.AudioMinus2			Octave -2 in dB(A)
	S.AudioMinus1			Octave -1 in dB(A)
	S.Audio0				Octave 0 in dB(A)
	S.AudioPlus1			Octave +1 in dB(A)
	S.AudioPlus2			Octave +2 in dB(A)
	S.AudioPlus3			Octave +3 in dB(A)
	S.AudioPlus4			Octave +4 in dB(A)
	S.AudioPlus5			Octave +5 in dB(A)
	S.AudioPlus6			Octave +6 in dB(A)
	S.AudioPlus7			Octave +7 in dB(A)
	S.AudioPlus8			Octave +8 in dB(A)
	S.AudioPlus9			Octave +9 in dB(A)
	S.AudioPlus10			Octave +10 in dB(A)
	S.SatInfo
	S.Latitude				nibbles: n1:0=East/North, 8=West/South; n2&n3: whole degrees (0-180); n4-n8: degree fraction (max 999999)
	S.Longitude				nibbles: n1:0=East/North, 8=West/South; n2&n3: whole degrees (0-180); n4-n8: degree fraction (max 999999)

	P.Powerstate					Power State
	P.BatteryVoltage				Battery Voltage (milliVolts)
	P.BatteryTemperature			Battery Temperature (milliKelvin)
	P.BatteryGauge					Get Battery Gauge, BFFF = Battery full, 1FFF = Battery fail, 0000 = No Battery Installed
	P.MuxStatus						Mux Status (0-7=channel,F=inhibited)
	P.ErrorStatus					Error Status (0=OK)
	P.BaseTimer						BaseTimer (seconds)
	P.SessionUptime					Session Uptime (seconds)
	P.TotalUptime					Total Uptime (minutes)
	v3: P.COHeaterMode				CO heater mode
	P.COHeater						Powerstate CO heater (0/1)
	P.NO2Heater						Powerstate NO2 heater (0/1)
	P.O3Heater						Powerstate O3 heater (0/1)
	v3: P.CO2Heater					Powerstate CO2 heater (0/1)
	P.UnitSerialnumber				Serialnumber of unit
	P.TemporarilyEnableDebugLeds	Debug leds (0/1)
	P.TemporarilyEnableBaseTimer	Enable BaseTime (0/1)
	P.ControllerReset				WIFI reset
	P.FirmwareUpdate				Firmware update, reboot to bootloader

	Unknown at this moment (decimal):
	P.11
	P.16
	P.17
	P.18

Below are typical values as obtained via the raw sensor API ::

	# General
	id: "20",
	p_unitserialnumber: 20,
	p_errorstatus: 0,
	p_powerstate: 2191,
	p_coheatermode: 167772549,

	# Date and time
	time: "2016-05-30T10:09:41.6655164Z",
	s_secondofday: 40245,
	s_rtcdate: 1069537,
	s_rtctime: 723501,
	p_totaluptime: 4409314,
	p_sessionuptime: 2914,
	p_basetimer: 6,

	# GPS
	s_longitude: 6071111,
	s_latitude: 54307269,
	s_satinfo: 86795,

	# Gas componements
	s_o3resistance: 30630,
	s_no2resistance: 160300,
	s_coresistance: 269275,

	# Meteo
	s_rain: 14,
	s_barometer: 100126,
	s_humidity: 75002,
	s_temperatureambient: 288837,
	s_temperatureunit: 297900,

	# Audio
	s_audioplus5: 1842974,
	v_audioplus4: 1578516,
	u_audioplus4: 1381393,
	t_audioplus4: 1907483,
	s_audioplus4: 1841174,
	v_audioplus3: 1710360,
	u_audioplus3: 1250066,
	t_audioplus3: 1842202,
	s_audioplus3: 1841946,
	v_audioplus2: 1381141,
	u_audioplus2: 1118225,
	t_audioplus2: 1645849,
	s_audioplus2: 1446679,
	v_audioplus1: 1381137,
	u_audioplus1: 1119505,
	t_audioplus1: 1776919,
	s_audioplus1: 1775382,
	v_audioplus9: 1710617,
	u_audioplus9: 1710617,
	t_audioplus9: 1841946,
	s_audioplus9: 1776409,
	v_audioplus8: 1512983,
	u_audioplus8: 1512982,
	t_audioplus8: 1578777,
	s_audioplus8: 1578776,
	v_audioplus7: 1381396,
	u_audioplus7: 1381396,
	t_audioplus7: 1512981,
	s_audioplus7: 1446932,
	v_audioplus6: 1249812,
	u_audioplus6: 1249555,
	t_audioplus6: 2036501,
	s_audioplus6: 1315604,
	v_audioplus5: 1776923,
	u_audioplus5: 1710360,
	t_audioplus5: 2171681,
	v_audio0: 1184000,
	u_audio0: 986112,
	t_audio0: 1513984,
	s_audio0: 1249536,

	# Light
	s_rgbcolor: 14546943,
	s_lightsensorblue: 13779,
	s_lightsensorgreen: 13352,
	s_lightsensorred: 11977,
	s_lightsensorbottom: 80,
	s_lightsensortop: 15981,

	# Accelerometer
	s_acceleroz: 783,
	s_acceleroy: 520,
	s_accelerox: 512,

	# Unknown
	p_6: 1382167
	p_11: 40286,
	p_18: 167772549,
	p_17: 167772549,


Below each of these sensor values are elaborated.
All conversions are implemented in using two Python scripts, called from the
Refiner ETL:

* `sensordefs.py <https://github.com/Geonovum/smartemission/blob/master/etl/sensordefs.py>`_ definitions of sensors
* `sensorconverters.py <https://github.com/Geonovum/smartemission/blob/master/etl/sensorconverters.py>`_ converter routines

By using a generic config file `sensordefs.py <https://github.com/Geonovum/smartemission/blob/master/etl/sensordefs.py>`_
all validation and calibration is specified generically. Below some sample entries. ::

	SENSOR_DEFS = {
	.
	.
	    # START Gasses Jose
	    's_o3resistance':
	        {
	            'label': 'O3Raw',
	            'unit': 'Ohm',
	            'min': 3000,
	            'max': 6000000
	        },
	    's_no2resistance':
	        {
	            'label': 'NO2RawOhm',
	            'unit': 'Ohm',
	            'min': 800,
	            'max': 20000000
	        },
	.
	.
	    # START Meteo Jose
	    's_temperatureambient':
	        {
	            'label': 'Temperatuur',
	            'unit': 'milliKelvin',
	            'min': 233150,
	            'max': 398150
	        },
	    's_barometer':
	        {
	            'label': 'Luchtdruk',
	            'unit': 'HectoPascal',
	            'min': 20000,
	            'max': 110000

	        },
	    's_humidity':
	        {
	            'label': 'Relative Humidity',
	            'unit': 'm%RH',
	            'min': 20000,
	            'max': 100000
	        },
	.
	.
	    'temperature':
	        {
	            'label': 'Temperatuur',
	            'unit': 'Celsius',
	            'input': 's_temperatureambient',
	            'converter': convert_temperature,
	            'type': int,
	            'min': -25,
	            'max': 60
	        },
	    'pressure':
	        {
	            'label': 'Luchtdruk',
	            'unit': 'HectoPascal',
	            'input': 's_barometer',
	            'converter': convert_barometer,
	            'type': int,
	            'min': 200,
	            'max': 1100
	        },
	    'humidity':
	        {
	            'label': 'Luchtvochtigheid',
	            'unit': 'Procent',
	            'input': 's_humidity',
	            'converter': convert_humidity,
	            'type': int,
	            'min': 20,
	            'max': 100
	        },
	    'noiseavg':
	        {
	            'label': 'Average Noise',
	            'unit': 'dB(A)',
	            'input': ['v_audio0', 'v_audioplus1', 'v_audioplus2', 'v_audioplus3', 'v_audioplus4', 'v_audioplus5',
	                      'v_audioplus6', 'v_audioplus7', 'v_audioplus8', 'v_audioplus9'],
	            'converter': convert_noise_avg,
	            'type': int,
	            'min': -100,
	            'max': 195
	        },
	    'noiselevelavg':
	        {
	            'label': 'Average Noise Level 1-5',
	            'unit': 'int',
	            'input': 'noiseavg',
	            'converter': convert_noise_level,
	            'type': int,
	            'min': 1,
	            'max': 5
	        },
	.
	.
	    'no2raw':
	        {
	            'label': 'NO2Raw',
	            'unit': 'kOhm',
	            'input': ['s_no2resistance'],
	            'min': 8,
	            'max': 4000,
	            'converter': ohm_to_kohm
	        },
	    'no2':
	        {
	            'label': 'NO2',
	            'unit': 'ug/m3',
	            'input': ['s_o3resistance', 's_no2resistance', 's_coresistance', 's_temperatureambient',
	                      's_temperatureunit', 's_humidity', 's_barometer', 's_lightsensorbottom'],
	            'converter': ohm_no2_to_ugm3,
	            'type': int,
	            'min': 0,
	            'max': 400
	        },
	    'o3raw':
	        {
	            'label': 'O3Raw',
	            'unit': 'kOhm',
	            'input': ['s_o3resistance'],
	            'min': 0,
	            'max': 20000,
	            'converter': ohm_to_kohm
	        },
	    'o3':
	        {
	            'label': 'O3',
	            'unit': 'ug/m3',
	            'input': ['s_o3resistance', 's_no2resistance', 's_coresistance', 's_temperatureambient',
	                      's_temperatureunit', 's_humidity', 's_barometer', 's_lightsensorbottom'],
	            'converter': ohm_o3_to_ugm3,
	            'type': int,
	            'min': 0,
	            'max': 400
	        },
	.
	.
	}

Each entry has:

* `label`: name for display
* `unit`: well the unit
* `input`: optionally one or more input Entries required for conversion (`sensorconverters.py <https://github.com/Geonovum/smartemission/blob/master/etl/sensorconverters.py>`_). May cascade.
* `converter`: pointer to Python conversion function
* `type`: value type
* `min/max`: valid range (for validation)

Entries starting with ``s_`` denote Jose raw sensor indicators. Others like ``no2`` are
"virtual" (SE) indicators, i.e. derived eventually from ``s_`` indicators.

In the `Refiner ETL-config <https://github.com/Geonovum/smartemission/blob/master/etl/refiner.cfg>`_ the
desired indicators are specified, for example:
``temperature,humidity,pressure,noiseavg,noiselevelavg,co2,o3,co,no2,o3raw,coraw,no2raw``.
In this fashion the Refiner remains generic: driven by required indicators and their Entries.

Gas Calibration with ANN
------------------------

Within the SE project a separate activity is performed for gas-calibration based on Big Data Analysis
statistical methods. Values coming from SE sensors were compared to actual RIVM values. By matching predicted
values with RIVM-values, a formula for each gas-component is established and refined. The initial approach
was to use linear analysis methods. However, further along in the project the use
of `Artificial Neural Networks (ANN) <https://en.wikipedia.org/wiki/Artificial_neural_network>`_
appeared to be the most promising.

Gas Calibration for SE is described more extensively in :ref:`calibration`.

Source code for ANN Gas Calibration: https://github.com/Geonovum/smartemission/tree/master/etl/calibration/src

GPS Data
--------

See https://github.com/Geonovum/sospilot/issues/22

Example: ::

	07/24/2015 07:27:36,S.Longitude,5914103
	07/24/2015 07:27:36,S.Latitude,53949937
	wordt

	Longitude: 5914103 --> 0x005a3df7
	0x05 --> 5 graden (n2 en n3),
	0xa3df7 --> 671223 (n4-n8) fractie --> 0.671223
	dus 5.671223 graden

	Latitude: 53949937 --> 0x033735f1
	0x33 --> 51 graden
	0x735f1 --> 472561 --> 0.472561
	dus 51.472561
	n0=0 klopt met East/North.
	5.671223, 51.472561

	komt precies uit in de Marshallstraat in Helmond bij Intemo, dus alles lijkt te kloppen!!

	In TypeScript:

	/*
	        8 nibbles:
	        MSB                  LSB
	        n1 n2 n3 n4 n5 n6 n7 n8
	        n1: 0 of 8, 0=East/North, 8=West/South
	        n2 en n3: whole degrees (0-180)
	        n4-n8: fraction of degrees (max 999999)
	*/
	private convert(input: number): number {
	 var sign = input >> 28 ? -1 : +1;
	 var deg = (input >> 20) & 255;
	 var dec = input & 1048575;

	 return (deg + dec / 1000000) * sign;
	}

In Python: ::

	# Lat or longitude conversion
	# 8 nibbles:
	# MSB                  LSB
	# n1 n2 n3 n4 n5 n6 n7 n8
	# n1: 0 of 8, 0=East/North, 8=West/South
	# n2 en n3: whole degrees (0-180)
	# n4-n8: fraction of degrees (max 999999)
	def convert_coord(input, json_obj, name):
	    sign = 1.0
	    if input >> 28:
	        sign = -1.0
	    deg = float((input >> 20) & 255)
	    dec = float(input & 1048575)

	    result = (deg + dec / 1000000.0) * sign
	    if result == 0.0:
	        result = None
	    return result

	def convert_latitude(input, json_obj, name):
	    res = convert_coord(input, json_obj, name)
	    if res is not None and (res < -90.0 or res > 90.0):
	        log.error('Invalid latitude %d' % res)
	        return None
	    return res

	def convert_longitude(input, json_obj, name):
	    res = convert_coord(input, json_obj, name)
	    if res is not None and (res < -180.0 or res > 180.0):
	        log.error('Invalid longitude %d' % res)
	        return None
	    return res

Meteo Data
----------

Python code: ::

	def convert_temperature(input, json_obj, name):
	    if input == 0:
	        return None

	    tempC = int(round(float(input)/1000.0 - 273.1))
	    if tempC > 100:
	        return None

	    return tempC


	def convert_barometer(input, json_obj, name):
	    result = float(input) / 100.0
	    if result > 2000:
	        return None
	    return int(round(result))


	def convert_humidity(input, json_obj, name):
	    humPercent = int(round(float(input) / 1000.0))
	    if humPercent > 100:
	        return None
	    return humPercent

Publisher
=========

The ``Publisher`` ETL process reads "Refined" indicator data and publishes
these to various web-services. Most specifically this entails publication to:

* OGC Sensor Observation Service (SOS)
* OGC Sensor Things API (STA)

For both SOS and STA the transactional/REST web-services are used.

Publishing to OGC WMS and WFS is not explicitly required: these
services can directly use the PostGIS database tables and VIEWs
produced by the ``Refiner``. For WMS, GeoServer WMS Dimension for the "time" column is
used together with SLDs that show values, in order to provide historical data via WMS.
WFS can be used for bulk download.

General
-------

The ETL chain is setup using the `smartemdb.RefinedDbInput` class directly coupled
to a Stetl Output class, specific for the web-service published to.

Sensor Observation Service (SOS)
--------------------------------

The `sosoutput.SOSTOutput` class is used to publish to a(ny) SOS using the standardized
SOS-Transactional web-service. The implementation is reasonably straightforward, with the following
specifics:

``JSON``: JSON is used as encoding for SOS-T requests

``Lazy sensor insertion``: If `InsertObservation` returns HTTP statuscode 400 an `InsertSensor`
request is submitted. If that is succesful the same `InsertObservation` is attempted again.

``SOS-T Templates``: all SOS-T requests are built using template files. In these files a complete
request is contained, with specific parameters, like `station_id` symbolically defined. At publication
time these are substituted.  Below an excerpt of an `InsertObservation` template: ::

	{{
	  "request": "InsertObservation",
	  "service": "SOS",
	  "version": "2.0.0",
	  "offering": "offering-{station_id}",
	  "observation": {{
	    "identifier": {{
	      "value": "{unique_id}",
	      "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"
	    }},
	    "type": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
	    "procedure": "station-{station_id}",
	    "observedProperty": "{component}",
	    "featureOfInterest": {{
	      "identifier": {{
	        "value": "fid-{station_id}",
	        "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"
        .
        .


Deleting SOS Entities
~~~~~~~~~~~~~~~~~~~~~

Also re-init of the 52North SOS DB is possible via the
`sos-clear.py script <https://github.com/Geonovum/smartemission/blob/master/services/sos52n/config/sos-clear.py>`_
(use with care!). This needs to go hand-in-hand with
a `restart of the SOS Publisher <https://github.com/Geonovum/smartemission/blob/master/etl/db/sos-publisher-init.sh>`_ .

Implementation
~~~~~~~~~~~~~~

Below are links to the sources of the SOS Publisher implementation.

* ETL run script: https://github.com/Geonovum/smartemission/blob/master/etl/sospublisher.sh
* Stetl conf: https://github.com/Geonovum/smartemission/blob/master/etl/sospublisher.cfg
* Refined DB Input: https://github.com/Geonovum/smartemission/blob/master/etl/smartemdb.py
* SOS-T publication: https://github.com/Geonovum/smartemission/blob/master/etl/sosoutput.py
* SOS-T templates: https://github.com/Geonovum/smartemission/blob/master/etl/sostemplates
* Input database schema: https://github.com/Geonovum/smartemission/blob/master/etl/db/db-schema-refined.sql (source input schema)
* Re-init SOS DB schema (.sh): https://github.com/Geonovum/smartemission/blob/master/services/sos52n/config/sos-clear.py
* Restart SOS Publisher (.sh): https://github.com/Geonovum/smartemission/blob/master/etl/db/sos-publisher-init.sh  (inits last gis published to -1)

Sensor Things API (STA)
-----------------------

The `STAOutput <https://github.com/Geonovum/smartemission/blob/master/etl/staoutput.py>`_ class
is used to publish to any SensorThings API server using the standardized
`OGC SensorThings REST API <http://docs.opengeospatial.org/is/15-078r6/15-078r6.html>`_.
The implementation is reasonably straightforward, with the following specifics:

``JSON``: JSON is used as encoding for STA requests.

``Lazy Entity Insertion``: At ``POST Observation`` it is determined via a REST GET requests if the corresponding
STA Entities, ``Thing``, ``Location``, ``DataStream`` etc are present. If not these are inserted
via ``POST`` requests to the STA REST API and cached locally in the ETL process for the duration
of the ``ETL Run``.

``STA Templates``: all STA requests are built using
`STA template files <https://github.com/Geonovum/smartemission/blob/master/etl/statemplates>`_.
In these files a complete request body (POST or PATCH)
is contained, with specific parameters, like ``station_id`` symbolically defined. At publication
time these are substituted.

Below the ``POST Location`` STA template: ::

	{{
	  "name": "{station_id}",
	  "description": "Location of Station {station_id}",
	  "encodingType": "application/vnd.geo+json",
	  "location": {{
	     "coordinates": [{lon}, {lat}],
	     "type": "Point"
	  }}
	}}

	{{

The ``location_id`` is returned from the GET. NB ``Location`` may also be ``PATCHed`` if
the  ``Location`` of the ``Thing`` has changed.

Below the ``POST Thing`` STA template: ::

	{{
	    "name": "{station_id}",
	    "description": "Smart Emission station {station_id}",
	    "properties": {{
	      "id": "{station_id}"
	    }},
	    "Locations": [
	        {{
	          "@iot.id": {location_id}
	        }}
	    ]
	}}

Similarly ``DataStream``, ``ObservedProperty`` are POSTed if non-existing.
Finally the ``POST Observation`` STA template: ::

	{{
	  "Datastream": {{
	    "@iot.id": {datastream_id}
	  }},
	  "phenomenonTime": "{sample_time}",
	  "result": {sample_value},
	  "resultTime": "{sample_time}",
	  "parameters": {{
	      {parameters}
	  }}
	}}

Deleting STA Entities
~~~~~~~~~~~~~~~~~~~~~

Also deletion of all Entities is possible via the
`staclear.py script <https://github.com/Geonovum/smartemission/blob/master/etl/db/staclear.py>`_
(use with care!). This needs to go hand-in-hand with
a `restart of the STA Publisher <https://github.com/Geonovum/smartemission/blob/master/etl/db/sta-publisher-init.sh>`_ .

Implementation
~~~~~~~~~~~~~~

Below are links to the sources of the STA Publisher implementation.

* ETL run script: https://github.com/Geonovum/smartemission/blob/master/etl/stapublisher.sh
* Stetl conf: https://github.com/Geonovum/smartemission/blob/master/etl/stapublisher.cfg
* Refined DB Input: https://github.com/Geonovum/smartemission/blob/master/etl/smartemdb.py
* STA publication: https://github.com/Geonovum/smartemission/blob/master/etl/staoutput.py
* STA templates: https://github.com/Geonovum/smartemission/blob/master/etl/statemplates
* Input database schema: https://github.com/Geonovum/smartemission/blob/master/etl/db/db-schema-refined.sql (source schema)
* Restart STA publisher (.sh): https://github.com/Geonovum/smartemission/blob/master/etl/db/sta-publisher-init.sh  (inits last gis published to -1)
* Clear/init STA server (.sh): https://github.com/Geonovum/smartemission/blob/master/etl/db/staclear.sh  (deletes all Entities!)
* Clear/init STA server (.py): https://github.com/Geonovum/smartemission/blob/master/etl/db/staclear.py  (deletes all Entities!)
