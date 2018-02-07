.. _cookbook:

========
Cookbook
========

This chapter contains sections to aid developers to interact with the SE platform.
This is split into the following areas:

* developing (web) clients that use the OGC web services (WFS, WMS, SOS, STA)
* developing new sensor types
* deploying subsets of the SE platform

Developing Web Clients
----------------------

The SE platform supports various standard OGC web APIs:

* WMS with Time Dimensions
* WFS
* Sensor Observation Service (SOS)
* SensorThings API (STA)

The use of STA is favoured over SOS.

SensorThings API
----------------

The easiest way to get data out of the SE Platform is via the `SensorThings API <http://docs.opengeospatial.org/is/15-078r6/15-078r6.html>`_.
As this API is REST-based one can already navigate through its enities via the web browser.
For example the URL http://data.smartemission.nl/gost/v1.0 will show all `Entities`. Each can be clicked
to navigate through the model.

Resources:

* `SensorThings API OGC Standard <http://docs.opengeospatial.org/is/15-078r6/15-078r6.html>`_
* http://ogc-iot.github.io/ogc-iot-api/datamodel.html - datamodel explanation
* http://developers.sensorup.com/docs/ - developer-friendly API docs, including JavaScript/cURL examples
* https://gost1.docs.apiary.io - STA GOST-provided API docs
* https://sensorup.atlassian.net/wiki/spaces/SPS - some more examples

The mapping of the STA entities is as follows:

* `Thing`: corresponds to single SE Device (Station)
* `Location`: holds single/last geographical Point location of Thing, thus SE Device
* `Datastream`:  corresponds to single indicator (e.g. Temperature or NO2) of single/specific SE Device
* `Observation`: corresponds to single measurement (e.g. Temperature or NO2) of single/specific `Datastream`
* `Sensor` and `ObservedProperty` provide metadata for a single/specific SE device indicator (mostly a sensor) thus `Datastream`

So a single `Thing` has multiple Datastreams, each `Datastream` provides multiple
`Observations` for a single `Sensor` and single `ObservedProperty`.
This corresponds to a single SE Device containing multiple indicators (mostly sensors) where each
indicator provides multiple measurements. Thus `Thing`, `Datastream` and `Observation` will be the three Entities mostly
used.

In addition for a `Thing` in SE the following conventions apply:

* `name` attribute corresponds to SE Device id
* `properties` is a free-form key/value list field using

 - `device_meta`: device type and version e.g. `jose-1`
 - `id`: device type and version e.g. `jose-1`
 - `last_update`: last date/time update was received from device
 - `project_id`: project identifier within SE (first 4 numbers of SE Device id)

Example properties: ::

	"properties": {
		"device_meta": "jose-1",
		"id": "20060009",
		"last_update": "2018-02-01T15:00:00+01:00",
		"project_id": 2006
	},

One caveat: as the STA GOST server holds over 5 million Entities (mainly `Observations`), most STA REST calls will
automatically provide `Paging` with a maximum of N (top or nested) Entities per page.
For example, getting all `Things` via http://data.smartemission.nl/gost/v1.0/Things gives: ::

	{
	   "@iot.count": 182,
	   "@iot.nextLink": "http://data.smartemission.nl/gost/v1.0/Things?$top=100&$skip=100",
	   "value": [
	      {
	         "@iot.id": 182,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Things(182)",
	         "name": "20060009",
	         "description": "Smart Emission station 20060009",
	         "properties": {
	            "device_meta": "jose-1",
	            "id": "20060009",
	            "last_update": "2018-02-01T15:00:00+01:00",
	            "project_id": 2006
	         },
	         "Locations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(182)/Locations",
	         "Datastreams@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(182)/Datastreams",
	         "HistoricalLocations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(182)/HistoricalLocations"
	      },
	      {
	         "@iot.id": 181,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Things(181)",
	         "name": "20060005",
	         "description": "Smart Emission station 20060005",
	         "properties": {
	            "device_meta": "jose-1",
	            "id": "20060005",
	            "last_update": "2018-02-01T15:00:00+01:00",
	            "project_id": 2006
	         },
	         "Locations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(181)/Locations",
	         "Datastreams@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(181)/Datastreams",
	         "HistoricalLocations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(181)/HistoricalLocations"
	      },
		.
		.
	      {
	         "@iot.id": 83,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Things(83)",
	         "name": "88",
	         "description": "Smart Emission station 88",
	         "properties": {
	            "device_meta": "jose-1",
	            "id": "88",
	            "last_update": "2018-01-25T07:00:00+01:00",
	            "project_id": 0
	         },
	         "Locations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(83)/Locations",
	         "Datastreams@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(83)/Datastreams",
	         "HistoricalLocations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(83)/HistoricalLocations"
	      }
	   ]
	}

where `"@iot.count": 182` denotes that there are 182 `Things` (SE Sensor Stations/Devices).

Paging: http://data.smartemission.nl/gost/v1.0/Things?$top=100&$skip=100 links to the next `Page` with `$top=100&$skip=100` indicating
show at most 100 Entities (`$top=100`) and skip the first 100 (`$skip=100`). The number 100 is a limit set in in the `GOST`
config file: `maxEntityResponse: 100`. One should always be aware of Paging.

Useful Queries
~~~~~~~~~~~~~~

Reminder: Paging will apply to the total number of Entities returned: so when e.g. `$expand`-ing Things,
the count will apply to the expanded Entities!

Getting a specific `Thing` by station id using `$filter`.:

  `http://data.smartemission.nl/gost/v1.0/Things?$filter=name eq '20010001' <http://data.smartemission.nl/gost/v1.0/Things?$filter=name%20eq%20%2720010001%27>`_

or URL-encoded:

  http://data.smartemission.nl/gost/v1.0/Things?$filter=name%20eq%20%2720010001%27

Getting Things expanding `Locations`, useful to plot e.g. SE Devices with (last) locations on a map:

  http://data.smartemission.nl/gost/v1.0/Things?$expand=Locations

Same, but requesting a more compact response (less attributes) using the `$select` option:

  http://data.smartemission.nl/gost/v1.0/Things?$expand=Locations($select=location)&$select=id,name

Result: ::

	{
	   "@iot.count": 182,
	   "@iot.nextLink": "http://data.smartemission.nl/gost/v1.0/Things?$expand=Locations($select=location)&$top=100&$skip=100",
	   "value": [
	      {
	         "@iot.id": 182,
	         "name": "20060009",
	         "Locations": [
	            {
	               "location": {
	                  "coordinates": [
	                     -2.048575,
	                     -2.048575
	                  ],
	                  "type": "Point"
	               }
	            }
	         ]
	      },
	      {
	         "@iot.id": 181,
	         "name": "20060005",
	         "Locations": [
	            {
	               "location": {
	                  "coordinates": [
	                     5.671203,
	                     51.47254
	                  ],
	                  "type": "Point"
	               }
	            }
	         ]
	      },
			.
			.
	      {
	         "@iot.id": 83,
	         "name": "88",
	         "Locations": [
	            {
	               "location": {
	                  "coordinates": [
	                     5.865303,
	                     51.846375
	                  ],
	                  "type": "Point"
	               }
	            }
	         ]
	      }
	   ]
	}


Getting all `Things` with `Locations` with specific `property`, for example all Devices for SE project `2001` (city of Zoetermeer):

  `http://data.smartemission.nl/gost/v1.0/Things?$filter=properties/project_id eq '2001'&$expand=Locations <http://data.smartemission.nl/gost/v1.0/Things?$filter=properties/project_id%20eq%20%272001%27&$expand=Locations>`_

or all SE Nijmegen project (0) Devices:

  `http://data.smartemission.nl/gost/v1.0/Things?$filter=properties/project_id% eq '0'&$expand=Locations <http://data.smartemission.nl/gost/v1.0/Things?$filter=properties/project_id%20eq%20%270%27&$expand=Locations>`_

Getting Things expanding `Locations` and `Datastreams` is often useful to plot e.g. Station icons on a map, also
providing info on all Indicators (`Datastreams`):

  http://data.smartemission.nl/gost/v1.0/Things?$expand=Locations,Datastreams

Result:  ::

	{
	   "@iot.count": 182,
	   "@iot.nextLink": "http://data.smartemission.nl/gost/v1.0/Things?$expand=Locations,Datastreams&$top=100&$skip=100",
	   "value": [
	      {
	         "@iot.id": 182,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Things(182)",
	         "name": "20060009",
	         "description": "Smart Emission station 20060009",
	         "properties": {
	            "device_meta": "jose-1",
	            "id": "20060009",
	            "last_update": "2018-02-01T15:00:00+01:00",
	            "project_id": 2006
	         },
	         "HistoricalLocations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Things(182)/HistoricalLocations",
	         "Locations": [
	            {
	               "@iot.id": 182,
	               "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Locations(182)",
	               "name": "20060009",
	               "description": "Location of Station 20060009",
	               "encodingType": "application/vnd.geo+json",
	               "location": {
	                  "coordinates": [
	                     -2.048575,
	                     -2.048575
	                  ],
	                  "type": "Point"
	               },
	               "Things@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Locations(182)/Things",
	               "HistoricalLocations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Locations(182)/HistoricalLocations"
	            }
	         ],
	         "Datastreams": [
	            {
	               "@iot.id": 1690,
	               "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1690)",
	               "name": "pm2_5",
	               "description": "PM 2.5 for Station 20060009",
	               "unitOfMeasurement": {
	                  "definition": "http://unitsofmeasure.org/ucum.html#para-30",
	                  "name": "PM 2.5",
	                  "symbol": "ug/m3"
	               },
	               "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
	               "Thing@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1690)/Thing",
	               "Sensor@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1690)/Sensor",
	               "Observations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1690)/Observations",
	               "ObservedProperty@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1690)/ObservedProperty"
	            },
	            {
	               "@iot.id": 1689,
	               "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1689)",
	               "name": "pm10",
	               "description": "PM 10 for Station 20060009",
	               "unitOfMeasurement": {
	                  "definition": "http://unitsofmeasure.org/ucum.html#para-30",
	                  "name": "PM 10",
	                  "symbol": "ug/m3"
	               },
	               "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
	               "Thing@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1689)/Thing",
	               "Sensor@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1689)/Sensor",
	               "Observations@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1689)/Observations",
	               "ObservedProperty@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Datastreams(1689)/ObservedProperty"
	            },

Getting specific `Datastreams` for single Indicator, for example getting all NO2 `Datastreams`.

	`http://data.smartemission.nl/gost/v1.0/Datastreams?$filter=name eq 'no2' <http://data.smartemission.nl/gost/v1.0/Datastreams?$filter=name%20eq%20%27no2%27>`_

**Getting Observations**

Getting last `Observations` since date/time:

  `http://data.smartemission.nl/gost/v1.0/Observations?$filter=phenomenonTime gt '2018-02-06T08:00:00.000Z' <http://data.smartemission.nl/gost/v1.0/Observations?$filter=phenomenonTime%20gt%20%272018-02-06T08:00:00.000Z%27>`_

Result: ::

	{
	   "@iot.count": 921,
	   "@iot.nextLink": "http://data.smartemission.nl/gost/v1.0/Observations?$filter=phenomenonTime gt '2018-02-06T08:00:00.000Z'&$top=100&$skip=100",
	   "value": [
	      {
	         "@iot.id": 5131983,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131983)",
	         "phenomenonTime": "2018-02-06T10:00:00.000Z",
	         "result": 1,
	         "parameters": {
	            "device_meta": "jose-1",
	            "gid": 5132008,
	            "name": "noiselevelavg",
	            "raw_gid": 492353,
	            "sensor_meta": "au-V30_V3F",
	            "station": 20000001
	         },
	         "Datastream@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131983)/Datastream",
	         "FeatureOfInterest@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131983)/FeatureOfInterest",
	         "resultTime": "2018-02-06T11:00:00+01:00"
	      },
	      {
	         "@iot.id": 5131982,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131982)",
	         "phenomenonTime": "2018-02-06T10:00:00.000Z",
	         "result": 1017,
	         "parameters": {
	            "device_meta": "jose-1",
	            "gid": 5132007,
	            "name": "pressure",
	            "raw_gid": 492353,
	            "sensor_meta": "press-S16",
	            "station": 20000001
	         },
	         "Datastream@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131982)/Datastream",
	         "FeatureOfInterest@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131982)/FeatureOfInterest",
	         "resultTime": "2018-02-06T11:00:00+01:00"
	      },

In the `parameters` some SE-specific data is encapsulated:

* `"device_meta": "jose-1"` - the Device type and -version
* `"gid": 5132007` - the original key from the `smartem_refined.timeseries` DB schema/table
* `"name": "pressure"` - the friendly name of the Indicator
* `"raw_gid": 492353` - the original key from the `smartem_raw.timeseries` DB schema/table
* `"sensor_meta": "press-S16"` - sensor type within the Device
* `"station": 20000001` - the Device id


Getting last `Observations` for a specific Device (`Thing`) is a common scenario.
Think of a web viewer:

- on opening the viewer all Devices are shown as icons on map
- clicking on an icon shows all last measurements (Observations) for all `Datastreams` of the `Thing`

One can first all `Datastreams` for a `Thing`, and
then for each `Datastream` get the last `Observation` using `$top=1`. Example for Device `20010001`:

1. Get the `Thing` for example by Device id, expanding `Datastreams`:

	`http://data.smartemission.nl/gost/v1.0/Things?$filter=name eq '20010001'&$expand=Datastreams <http://data.smartemission.nl/gost/v1.0/Things?$filter=name%20eq%20%2720010001%27&$expand=Datastreams>`_

2. Now get the last `Observation` for each `Datastream`

  PM10: http://data.smartemission.nl/gost/v1.0/Datastreams(1255)/Observations?$top=1

  PM2_5: http://data.smartemission.nl/gost/v1.0/Datastreams(1254)/Observations?$top=1

A more direct way to get the last `Observation` for each `Datastream` from a `Thing` queried by `device_id` in a single GET:

  `http://data.smartemission.nl/gost/v1.0/Things?$filter=name eq '20010001'&$expand=Datastreams/Observations($top=1) <http://data.smartemission.nl/gost/v1.0/Things?$filter=name%20eq%20%2720010001%27&$expand=Datastreams/Observations($top=1)>`_

Or when the `Thing` id (`131` here) is known, simpler:

  `http://data.smartemission.nl/gost/v1.0/Things(131)?$expand=Datastreams/Observations($top=1) <http://data.smartemission.nl/gost/v1.0/Things(131)?$expand=Datastreams/Observations($top=1)>`_

Using `$select`, to receive less data attributes. Here query for Device id `20010001` last `Observations` showing only `id` and `name` of each `Datastream`:

  `http://data.smartemission.nl/gost/v1.0/Things?$filter=name eq '20010001'&$select=id,name&$expand=Datastreams($select=id,name),Datastreams/Observations($top=1) <http://data.smartemission.nl/gost/v1.0/Things?$filter=name%20eq%20%2720010001%27&$select=id,name&$expand=Datastreams($select=id,name),Datastreams/Observations($top=1)>`_

Result: ::

	{
	   "@iot.count": 1,
	   "value": [
	      {
	         "@iot.id": 131,
	         "name": "20010001",
	         "Datastreams": [
	            {
	               "@iot.id": 1255,
	               "name": "pm10",
	               "Observations": [
	                  {
	                     "@iot.id": 5145885,
	                     "phenomenonTime": "2018-02-07T11:00:00.000Z",
	                     "result": 137,
	                     "parameters": {
	                        "device_meta": "jose-1",
	                        "gid": 5145910,
	                        "name": "pm10",
	                        "raw_gid": 493875,
	                        "sensor_meta": "pm10-S29",
	                        "station": 20010001
	                     },
	                     "resultTime": "2018-02-07T12:00:00+01:00"
	                  }
	               ]
	            },
	            {
	               "@iot.id": 1254,
	               "name": "pm2_5",
	               "Observations": [
	                  {
	                     "@iot.id": 5145881,
	                     "phenomenonTime": "2018-02-07T11:00:00.000Z",
	                     "result": 122,
	                     "parameters": {
	                        "device_meta": "jose-1",
	                        "gid": 5145906,
	                        "name": "pm2_5",
	                        "raw_gid": 493875,
	                        "sensor_meta": "pm2_5-S2A",
	                        "station": 20010001
	                     },
	                     "resultTime": "2018-02-07T12:00:00+01:00"
	                  }
	               ]
	            },
				.
				.
	            {
	               "@iot.id": 1248,
	               "name": "noiseavg",
	               "Observations": [
	                  {
	                     "@iot.id": 5145882,
	                     "phenomenonTime": "2018-02-07T11:00:00.000Z",
	                     "result": 47,
	                     "parameters": {
	                        "device_meta": "jose-1",
	                        "gid": 5145907,
	                        "name": "noiseavg",
	                        "raw_gid": 493875,
	                        "sensor_meta": "au-V30_V3F",
	                        "station": 20010001
	                     },
	                     "resultTime": "2018-02-07T12:00:00+01:00"
	                  }
	               ]
	            }
	         ]
	      }
	   ]
	}

Last 100 Observations from any Indicators from any Devices:

  http://data.smartemission.nl/gost/v1.0/Observations?$top=100

Result: ::

	{
	   "@iot.count": 5131983,
	   "@iot.nextLink": "http://data.smartemission.nl/gost/v1.0/Observations?$top=100&$skip=100",
	   "value": [
	      {
	         "@iot.id": 5131983,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131983)",
	         "phenomenonTime": "2018-02-06T10:00:00.000Z",
	         "result": 1,
	         "parameters": {
	            "device_meta": "jose-1",
	            "gid": 5132008,
	            "name": "noiselevelavg",
	            "raw_gid": 492353,
	            "sensor_meta": "au-V30_V3F",
	            "station": 20000001
	         },
	         "Datastream@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131983)/Datastream",
	         "FeatureOfInterest@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131983)/FeatureOfInterest",
	         "resultTime": "2018-02-06T11:00:00+01:00"
	      },
	      {
	         "@iot.id": 5131982,
	         "@iot.selfLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131982)",
	         "phenomenonTime": "2018-02-06T10:00:00.000Z",
	         "result": 1017,
	         "parameters": {
	            "device_meta": "jose-1",
	            "gid": 5132007,
	            "name": "pressure",
	            "raw_gid": 492353,
	            "sensor_meta": "press-S16",
	            "station": 20000001
	         },
	         "Datastream@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131982)/Datastream",
	         "FeatureOfInterest@iot.navigationLink": "http://data.smartemission.nl/gost/v1.0/Observations(5131982)/FeatureOfInterest",
	         "resultTime": "2018-02-06T11:00:00+01:00"
	      },

** Get Observations using date/time **

The field `phenomenonTime` of Observation denotes the date/time of the original Observation.

As the Observations in the SE GOST server always denote hourly averages the   `phenomenonTime` applies to the
*previous hour* of the  `phenomenonTime`. Best, in terms of response times, is to use explicit intervals with the
`ge, gt` and `le, lt` operators. At this time using ISO 8601 intervals results in long response times.

To get all `Observations` of a specific hour let's say between 11:00 and 12:00 on January 29, 2018:

  `http://data.smartemission.nl/gost/v1.0/Observations?$filter=phenomenonTime gt '2018-01-29T11:00:00.000Z' and phenomenonTime le '2018-01-29T12:00:00.000Z'&$select=result,phenomenonTime,parameters <http://data.smartemission.nl/gost/v1.0/Observations?$filter=phenomenonTime%20gt%20%272018-01-29T11:00:00.000Z%27%20and%20%20phenomenonTime%20le%20%272018-01-29T12:00:00.000Z%27&$select=result,phenomenonTime,parameters>`_

This can also be used to get the latest Observations.
