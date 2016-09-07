.. _services:

============
Web Services
============

This chapter describes how various OGC OWS web services are realized on top of the
converted/transformed data as described in the `data chapter <data.html>`_.
In particular:

* WFS and WMS-Time services
* OWS SOS (REST) service
* SensorThings API

Architecture
============

Figure 1 sketches the overall architecture with emphasis on the flow of data (arrows).
Circles depict harvesting/ETL processes. Server-instances are in rectangles. Datastores
the "DB"-icons.

TBS

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

For the SensorThings API the SensorUp STA implementation is used.





