.. _data:

===============
Data Management
===============

This chapter describes all technical aspects related to data/ETL within the Smart Emission Data Platform
based on the (ETL-)design described within the :ref:`architecture` chapter.

Conversions
===========

Most raw sensor values as harvested from the CityGIS-platform need to be converted
and calibrated to units and values that approximate the "real situation" as much as possible.
Especially for gas-components this may be a challenge. Here raw sensor-values are expressed in
kOhms (NO2, O3 and CO) except for CO2 which is given in ppb. Audio-values are already provided in decibels.
Meteo-values are more standard and obvious to convert (e.g. milliKelvin to deegree Celsius).

The complexity for the calibration of gasses lies in the fact that many parameters may influence
measured values: temperature, relative humidity, pressure and even the concentration of
other gasses! For example O3 and NO2. A great deal of scientific literature is already devoted
to the sensor calibration issue.

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

Below each of these sensor values are elaborated. All conversions are implemented in this Python script and
used in various ETL-chains:
https://github.com/Geonovum/smartemission/blob/master/etl/sensorconverters.py

Gas Components
--------------

Within the SE project a seperate activity is performed for gas-calibration based on Big Data Analysis
statistical methods. Values coming from SE sensors were compared to actual RIVM values. By matching predicted
values with RIVM-values, a formula for each gas-component is established and refined.

This is all implemented and described in this GitHub repo:
https://github.com/pietermarsman/smartemission_calibration .

By using the R-language, reports in PDF are generated.

O3 Calibration
--------------

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



