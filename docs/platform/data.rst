.. _data:

===============
Data Management
===============

This chapter describes all technical aspects related to data/ETL within
the Smart Emission Data Platform
based on the (ETL-)design described within the :ref:`architecture` chapter.
As indicated there are three ETL-steps in sequence:

* Harvester - fetch raw sensor values from "Whale server"
* Refiner - validate, convert, calibrate and aggregate raw sensor values
* Publisher - publish refined values to various (OGC) services

Implementation for all ETL can be found here:
https://github.com/Geonovum/smartemission/blob/master/etl

The `ETL-framework Stetl <http://stetl.org>`_ is used for all ETL-steps using
ageneric `Stetl Docker Image <https://github.com/Geonovum/smartemission/blob/master/docker/stetl>`_
is reused in every ETL-step. Each of the three ETL-steps are expanded below.

Harvester
=========

To be supplied. Implementation:

* https://github.com/Geonovum/smartemission/blob/master/etl/harvester.sh
* https://github.com/Geonovum/smartemission/blob/master/etl/harvester.cfg
* https://github.com/Geonovum/smartemission/blob/master/etl/rawsensorapi.py
* database: https://github.com/Geonovum/smartemission/blob/master/etl/db/db-schema-raw.sql

The "Last" values ETL is an optimization/shorthand to provide all three ETL-steps
for only the last/current sensor values within a single ETL process. Implementation:

* https://github.com/Geonovum/smartemission/blob/master/etl/last.sh
* https://github.com/Geonovum/smartemission/blob/master/etl/last.cfg
* https://github.com/Geonovum/smartemission/blob/master/etl/rawsensorapi.py
* database: https://github.com/Geonovum/smartemission/blob/master/etl/db/db-schema-last.sql

Refiner
=======

Most raw sensor values as harvested from the CityGIS-platform need to be converted
and calibrated to units and values that approximate the "real situation" as much as possible.
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
All conversions are implemented in using two Python scripts, used in the Refiner ETL:

* `sensordefs.py <https://github.com/Geonovum/smartemission/blob/master/etl/sensordefs.py>`_ definitions of sensors
* `sensorconverters.py <https://github.com/Geonovum/smartemission/blob/master/etl/sensorconverters.py>`_ converter routines


Gas Components
--------------

Within the SE project a seperate activity is performed for gas-calibration based on Big Data Analysis
statistical methods. Values coming from SE sensors were compared to actual RIVM values. By matching predicted
values with RIVM-values, a formula for each gas-component is established and refined.

This is all implemented and described in this GitHub repo:
https://github.com/pietermarsman/smartemission_calibration .

By using the R-language, reports in PDF are generated.

O3 Calibration
~~~~~~~~~~~~~~

O3 seems to be the most linear. See the resulting `O3 PDF report <_static/calibration/O3.pdf>`_.

From the linear model comes the following formula for the conversion from resistance (kOhm) to ug/m3 (at 20C and 1013 hPa)  ::

	O3 = 89.1177
	+ 0.03420626 * s.coresistance * log(s.o3resistance)
	- 0.008836714 * s.light.sensor.bottom
	- 0.02934928 s.coresistance * s.temperature.ambient
	- 1.439367 * s.temperature.ambient * log(s.coresistance)
	+ 1.26521 * log(s.coresistance) * sqrt(s.coresistance)
	- 0.000343098 * s.coresistance * s.no2resistance
	+ 0.02761877 * s.no2resistance * log(s.o3resistance)
	- 0.0002260495 * s.barometer * s.coresistance
	+ 0.0699428 * s.humidity
	+ 0.008435412 * s.temperature.unit * sqrt(s.no2resistance)

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

To be supplied. Implementation:

* https://github.com/Geonovum/smartemission/blob/master/etl/publisher.sh
* https://github.com/Geonovum/smartemission/blob/master/etl/publisher.cfg
* https://github.com/Geonovum/smartemission/blob/master/etl/smartemdb.py
* https://github.com/Geonovum/smartemission/blob/master/etl/sosoutput.py
* database: https://github.com/Geonovum/smartemission/blob/master/etl/db/db-schema-refined.sql (source schema)
