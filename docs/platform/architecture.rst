.. _architecture:

============
Architecture
============

This chapter describes the (software) architecture of the Smart Emission Data Platform.

Docker
======

`Docker <https://www.docker.com>`_ is the main building block for the SE Data Platform deployment architecture.

`Docker <https://www.docker.com>`_
*...allows you to package an application with all of its dependencies into a standardized unit for software development.*.
Read more  on https://docs.docker.com.

The details of Docker are not discussed here, there are ample sources on the web. One of the best,
if not the best, introductory books on Docker is `The Docker Book <https://www.dockerbook.com>`_.

Docker Strategy
---------------

Like in Object Oriented Design there are still various strategies and patterns to follow with Docker.
There is a myriad of choices how to define Docker Images, configure and run Containers etc.
Within the SE Platform the following strategies are followed:

* define only generic/reusable Docker Images, i.e. without SE-specific config/functions
* let each Docker image perform a single (server) task: Apache2, GeoServer, PostGIS, 52NSOS etc.
* keep all configuration, data, logfiles and dynamic data outside Docker container on the Docker host
* at runtime provision the Docker Container with local mappings to data, ports and other Docker containers

Docker Containers
-----------------

The following Docker Containers are deployed. Also their related Docker Image is listed.

* ``web`` - web and webapps, proxy to backend - image: ``geonovum/apache2''
* ``postgis`` - PostgreSQL w PostGIS - image: ``kartoza/postgis:9.4-2.1``
* ``stetl`` - All ETL tasks - image: ``geonovum/stetl``
* ``geoserver`` - GeoServer web app - image:  ``kartoza/geoserver`` (TBD)
* ``sos52`` - 52NOrth SOS web app: ``kartoza/geoserver`` (TBD)