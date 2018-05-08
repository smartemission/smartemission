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

These components are deployed within `Kubernetes <https://kubernetes.io/>`_ (2018, Kadaster PDOK migration).

Overview
========

In the table below all Components are listed, their function,
source (GitHub, GH) and Docker (Hub, DH) repositories,
Categories, and for development strategy, their priority for the 2018
SE migration to Kubernetes (K8s). The "Status" column denotes the availability
of the Docker Image for K8s deployment:

* -=not yet started
* inprog=in progress
* avail=available for deploy
* done=deployed in K8s

================  =============  =================================  ======== ======= ========
Name              Categories     Function                           Repos    Prio    Status
================  =============  =================================  ======== ======= ========
Home              Apps           Platform home/landing page         GH DH    1       done
Admin             Apps,Admin     Admin access pages                 GH DH    2       done
Heron             Apps           Viewer with history                GH DH    1       done
SmartApp          Apps           Viewer for last values             GH DH    1       done
Waalkade          Apps           Viewer Nijmegen project            GH DH    1       done
GostDashboard     Apps,Admin     Admin dashboard Gost               GH DH    3       inprog
Grafana           Apps           View InfluxDB Data                 GH DH    3       inprog
Chronograf        Apps,Admin     Admin dashboard InfluxDB           GH DH    3       avail
SOSEmu            Services       REST API SOS subset                GH DH    1       done
GeoServer         Services       WMS (Time), WFS server             GH DH    1       done
Gost              Services       SensorThings API (STA) server      GH DH    2       done
SOS52N            Services       52North SOS server                 GH DH    3       done
Mosquitto         Services       MQTT server coupled with Gost      GH DH    2       done
PhpPgAdmin        Apps,Admin     Manager PostgreSQL                 GH DH    2       done
HarvesterLast     ETL            Harvester last sensor data         GH DH    1       done
HarvesterWhale    ETL            Harvester historic sensor data     GH DH    1       done
HarvesterInflux   ETL            Harvester InfluxDB sensor data     GH DH    3       inprog
HarvesterRivm     ETL            Harvester RIVM ANN ref-data        GH DH    4       avail
Extractor         ETL            Extract SE refdata for ANN ref     GH DH    4       avail
Calibrator        ETL            ANN Learning engine                GH DH    4       -
Refiner           ETL            Transformation/Calibration         GH DH    1       done
SOSPublisher      ETL            Publish refined data to SOS        GH DH    3       avail
STAPublisher      ETL            Publish refined data to STA        GH DH    2       done
InfluxDB          Datastore      Calibration refdata/collector      GH DH    3       -
PGPool            Datastore      PG Connection Pooling (only K8s)   GH DH    1       done
Postgis           Datastore      Main database (not used in K8s)    GH DH    N.A.    N.A.
Traefik           Services       Proxy server (not used in K8s)     GH DH    N.A.    N.A.
Prometheus        Mon,Apps       Monitoring metrics collector       GH DH    4       -
AlertManager      Mon            Prometheus (Prom.)alerter          GH DH    4       -
CAdvisor          Mon            Prom. Docker metrics exporter      GH DH    4       -
NodeExporter      Mon            Prom. host  metrics exporter       GH DH    4       -
GrafanaMon        Mon,Apps       Grafana Dashboards Prometheus      GH DH    4       -
================  =============  =================================  ======== ======= ========
