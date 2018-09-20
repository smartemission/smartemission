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

================  =============  =================================  =============================================================================================== ======= ========
Name              Categories     Function                           Repos                                                                                           Prio    Status
================  =============  =================================  =============================================================================================== ======= ========
Home              Apps           Platform home/landing page         `GH <https://github.com/smartemission/docker-se-home>`_ DH                                      1       done
Admin             Apps,Admin     Admin access pages                 `GH <https://github.com/smartemission/docker-se-admin>`_  DH                                    2       done
Heron             Apps           Viewer with history                `GH <https://github.com/smartemission/docker-se-heron>`_  DH                                    1       done
SmartApp          Apps           Viewer for last values             `GH <https://github.com/smartemission/docker-se-smartapp>`_ DH                                  1       done
Waalkade          Apps           Viewer Nijmegen project            `GH <https://github.com/smartemission/docker-se-waalkade>`_ DH                                  1       done
GostDashboard     Apps,Admin     Admin dashboard Gost               `GH <https://github.com/smartemission/docker-se-gostdashboard>`_ DH                             3       onhold
Grafana           Apps           View InfluxDB Data                 `GH <https://github.com/smartemission/docker-se-grafana>`_ DH                                   2       done
GrafanaDC         Apps           View InfluxDB Data Collector Data  `GH <https://github.com/smartemission/docker-se-grafana-dc>`_ DH                                2       done
Chronograf        Apps,Admin     Admin dashboard InfluxDB           `GH <https://https://www.influxdata.com/time-series-platform/chronograf/>`_ DH                  3       onhold
SOSEmu            Services       REST API SOS subset                `GH <https://github.com/smartemission/docker-se-sosemu>`_ DH                                    1       done
GeoServer         Services       WMS (Time), WFS server             `GH <https://github.com/smartemission/docker-se-geoserver>`_ DH                                 1       done
Gost              Services       SensorThings API (STA) server      `GH <https://github.com/smartemission/docker-se-gost>`_ DH                                      2       done
SOS52N            Services       52North SOS server                 `GH <https://github.com/smartemission/docker-se-sos52n>`_ DH                                    3       done
Mosquitto         Services       MQTT server coupled with Gost      `GH <https://github.com/smartemission/docker-se-mosquitto>`_ DH                                 2       done
PhpPgAdmin        Apps,Admin     Manager PostgreSQL                 `GH <https://github.com/smartemission/docker-se-phppgadmin>`_ DH                                2       done
HarvesterLast     ETL            Harvester last sensor data         `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     1       done
HarvesterWhale    ETL            Harvester historic sensor data     `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     1       inprog
HarvesterInflux   ETL            Harvester InfluxDB sensor data     `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     2       inprog
HarvesterRivm     ETL            Harvester RIVM ANN ref-data        `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     2       inprog
Extractor         ETL            Extract SE refdata for ANN ref     `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     2       inprog
Calibrator        ETL            ANN Learning engine                `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     2       -
Refiner           ETL            Transformation/Calibration         `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     1       inprog
SOSPublisher      ETL            Publish refined data to SOS        `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     3       inprog
STAPublisher      ETL            Publish refined data to STA        `GH <https://github.com/smartemission/docker-se-stetl>`_ DH                                     2       inprog
InfluxDB          Datastore      Calibration refdata/collector      `GH <https://github.com/smartemission/docker-se-influxdb>`_ DH                                  2       inprog
InfluxDB DC       Datastore      Data Collector AirSensEUR          `GH <https://github.com/smartemission/docker-se-influxdb>`_ DH                                  2       inprog
Postgis           Datastore      Main database (not used in K8s)    `GH <https://github.com/smartemission/docker-se-postgis>`_ DH                                   N.A.    N.A.
Traefik           Services       Proxy server (not used in K8s)     `GH <https://traefik.io/>`_ DH                                                                  N.A.    N.A.
Prometheus        Mon,Apps       Monitoring metrics collector       `GH <https://prometheus.io/>`_ DH                                                               4       -
AlertManager      Mon            Prometheus (Prom.)alerter          `GH <https://prometheus.io/docs/alerting/alertmanager/>`_ DH                                    4       -
CAdvisor          Mon            Prom. Docker metrics exporter      `GH <https://github.com/google/cadvisor>`_ DH                                                   4       -
NodeExporter      Mon            Prom. host  metrics exporter       `GH <https://github.com/prometheus/node_exporter>`_ DH                                          4       -
GrafanaMon        Mon,Apps       Grafana Dashboards Prometheus      `GH <https://github.com/smartemission/smartemission/tree/master/services/monitoring>`_ DH       4       -
================  =============  =================================  =============================================================================================== ======= ========
