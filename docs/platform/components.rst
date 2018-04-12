.. _components:

==========
Components
==========

This chapter gives an overview of all components within the SE Platform and
how they are organized into a (Docker/Kubernetes)
`microservices architecture <https://en.wikipedia.org/wiki/Microservices>`_.

A **Component** in this architecture is typically realized by a Docker Container
as a configured instance of its Docker Image. A Component typically provides a
**(micro)Service** and uses/depends on the services of other Components. A deployed Component
is as much self-contained as possible, for example a Component has no
host-specific dependencies like Volume mappings etc.

Docker Images for SE Components are maintained in the
`SE GitHub Organization <https://github.com/smartemission>`_ and
made available via the
`SE Docker Hub <https://hub.docker.com/r/smartemission>`_

Components are also divided into (functional) categories, being:

* **Apps** - user-visible web applications
* **Services** - API services providing spatiotemporal data (WMS, WFS, STA etc)
* **ETL** - data handling, conversions and transformations, ETL=Extract Transform Load
* **Datastore** - databases
* **Mon** - monitoring and healthchecking of the SE Platform
* **Admin** - administrative tools, access resticted to admin users

Some Components may fit in multiple categories. For example a Grafana App to visualize
monitoring data will be an App and Monitoring category.

Overview
========

In the table below all Components are listed, their function,
source (GitHub, GH) and Docker (Hub, DH) repositories,
Categories, and for development strategy, their priority for the 2018
SE migration to Kubernetes.

================  =============  ===============================  ======== =======
Name              Categories     Function                         Repos    Prio
================  =============  ===============================  ======== =======
Home              Apps           Platform home/landing page       GH DH    1
Admin             Apps,Admin     Admin access pages               GH DH    2
Heron             Apps           Viewer with history              GH DH    1
SmartApp          Apps           Viewer for last values           GH DH    1
Waalkade          Apps           Viewer Nijmegen project          GH DH    1
GostDashboard     Apps,Admin     Admin dashboard Gost             GH DH    3
Grafana           Apps           View InfluxDB Data               GH DH    3
Chronograf        Apps,Admin     Admin dashboard InfluxDB         GH DH    3
SOSEmu            Services       REST API SOS subset              GH DH    3
GeoServer         Services       WMS (Time), WFS server           GH DH    1
Gost              Services       SensorThings API (STA) server    GH DH    2
SOS52N            Services       52North SOS server               GH DH    3
Mosquitto         Services       MQTT server coupled with Gost    GH DH    2
PhpPgAdmin        Apps           Manager PostgreSQL               GH DH    2
HarvesterLast     ETL            Harvester last sensor data       GH DH    1
HarvesterWhale    ETL            Harvester historic sensor data   GH DH    1
HarvesterInflux   ETL            Harvester InfluxDB sensor data   GH DH    3
HarvesterRivm     ETL            Harvester RIVM ANN ref-data      GH DH    4
Extractor         ETL            Extract SE refdata for ANN ref   GH DH    4
Calibrator        ETL            ANN Learning engine              GH DH    4
Refiner           ETL            Transformation/Calibration       GH DH    1
SOSPublisher      ETL            Publish refined data to SOS      GH DH    3
STAPublisher      ETL            Publish refined data to STA      GH DH    2
InfluxDB          Datastore      Calibration refdata/collector    GH DH    3
Postgis           Datastore      Main database (not used in K8s)  GH DH    N.A.
Traefik           Services       Proxy server (not used in K8s)   GH DH    N.A.
Prometheus        Mon,Apps       Monitoring metrics collector     GH DH    3
AlertManager      Mon            Prometheus (Prom.)alerter        GH DH    3
CAdvisor          Mon            Prom. Docker metrics exporter    GH DH    3
NodeExporter      Mon            Prom. host  metrics exporter     GH DH    3
GrafanaMon        Mon,Apps       Grafana Dashboards Prometheus    GH DH    3
================  =============  ===============================  ======== =======
