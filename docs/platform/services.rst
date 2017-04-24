.. _services:

============
Web Services
============

This chapter describes how various OGC OWS web services are realized on top of the
converted/transformed data as described in the `data chapter <data.html>`_.
In particular:

* WFS and WMS-Time services
* OWS SOS (plus REST) service
* Smart Emission SOS Emulator service for Last Values
* SensorThings API
* InfluxDB
* Grafana

Web Frontend
============

All webservices, APIs and the website http://data.smartemission.nl are provided
via an Apache2 HTTP server. This server is the main outside entry to the platform
and run via Docker.

Website and Viewers are run as a standard HTML website. The various API/OGC web-services
are forwarded via proxies to the backed-servers. For example GeoServer
and the 52North SOS are connected via ``mod-proxy-ajp``.

The SOS Emulator for Last Values is hosted as a Python Flask app.

Implementation
--------------

* Docker image: https://github.com/Geonovum/smartemission/tree/master/docker/apache2
* Main dir: https://github.com/Geonovum/smartemission/tree/master/services/web
* Running: https://github.com/Geonovum/smartemission/tree/master/services/web/run.sh
* SOS Emulator: https://github.com/Geonovum/smartemission/tree/master/services/api/sosrest
* Website and Viewers: https://github.com/Geonovum/smartemission/tree/master/services/web/site
* Apache2 config: https://github.com/Geonovum/smartemission/tree/master/services/web/config/sites-enabled

WFS and WMS Services
====================

WMS and WFS are provided by GeoServer. These services are realized on top of the
PostGIS tables/VIEWs resulting from the ``Refiner`` ETL process for timeseries (history) based
layers and the "Last" table/VIEWs for Layers showing current values.

The OGC standard ``WMS-Dimension`` facility is used to provide WMS layers for timeseries (history).

SOS Services
============

*"The OGC Sensor Observation Service aggregates readings from live, in-situ and remote sensors.*
*The service provides an interface to make sensors and sensor data archives accessible via an*
*interoperable web based interface."*

The chapter on server administration describes how the SOS is deployed. This is
called here the 'SOS Server'.

The SOS server is provided using the 52North SOS web application (v4.3.7).

Docker for 52North SOS
----------------------

Deployment of this SOS via Docker required some specific Docker features in order
to deal with the 52North SOS configuration files.

During Docker build some specific configuration files are
copied permanently into the Docker image
as it is not possible to map these via symlinks from host. These files
are maintained in
GitHub https://github.com/Geonovum/smartemission/tree/master/docker/sos52n/resources/config:

* datasource.properties
* logback.xml
* timeseries-api_v1_beans.xml  (just for Service Identification)

The third config file that the SOS needs is `WEB-INF/configuration.db`.
In the Docker image this file is a symlink of `/opt/sosconfig/configuration.db`.
A default version is provided. However, to be able to maintain
this file over reruns of the Docker image a Docker volume mount should be
done within the service invokation. This is done lazily within the Docker
run file for the 52North SOS:
https://github.com/Geonovum/smartemission/blob/master/services/sos52n/run.sh
On the first run the `/opt/sosconfig` is mapped locally (plus the SOS log dir).
From then on `configuration.db` is maintained on the host.

At runtime the `sos52n` Docker instance is linked to the `postgis` Docker instance.

Implementation
--------------

* Docker image: https://github.com/Geonovum/smartemission/tree/master/docker/sos52n
* Running: https://github.com/Geonovum/smartemission/tree/master/services/sos52n

SensorThings API
================

For the SensorThings API the Geodan GOST STA implementation is used.
The GOST server is available at http://data.smartemission.nl/gost/v1.0.
The GOST Dashboard is available at http://data.smartemission.nl/gost/Dashboard/.

NB all modifying HTTP methods (POST, PUT, DELETE, PATCH) and the GOST Dashboard
are password-protected.

Implementation
--------------

* Docker image: https://hub.docker.com/r/geodan/gost/
* Running: https://github.com/Geonovum/smartemission/tree/master/services/gost

MQTT - Mosquitto
================

For the SensorThings API (GOST) MQTT is used. MQTT is a generic IoT protocol
that can be used in other contexts besides STA.

The MQTT server is available at http://data.smartemission.nl:1883
and http://data.smartemission.nl:9001

See also the GOST Dashboard at http://data.smartemission.nl/gost/Dashboard/.

Implementation
--------------

* Docker image: https://hub.docker.com/r/toke/mosquitto/
* Running: https://github.com/Geonovum/smartemission/tree/master/services/mosquitto

InfluxDB
========

InfluxDB has been added later in the project to support the Calibration process.
For now this service is used internally to collect both raw Sensor data and
calibrated RIVM data.

At a later stage InfluxDB may get a more central role in the platform.

Implementation
--------------

* Docker image: https://hub.docker.com/_/influxdb/
* Running: https://github.com/Geonovum/smartemission/tree/master/services/influxdb

Grafana
=======

Grafana has been added later in the project to support InfluxDB visualization.

At a later stage Grafana may get a more central role in the platform.

Implementation
--------------

* Docker image: https://github.com/grafana/grafana-docker
* Running: https://github.com/Geonovum/smartemission/tree/master/services/grafana
