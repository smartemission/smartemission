.. _admin:

==============
Administration
==============

This chapter describes the daily operation and maintenance aspects for the Smart Emission platform. For example:

* how to start stop servers
* backup and restore
* managing the ETL
* where to find logfiles
* troubleshooting
* monitoring

Backup
======

Backup is automated: see Platform cronfile.txt and the backup.sh script.

Only dynamic data is backed-up as all
code is in GitHub and the entire platform can be rebuild in minutes.

The last 7 days of data are backed-up by weekday (1 is monday), and then the last day of
each year-month. Backups can be accessed via ``sftp`` : ::

	$ sftp vps68271@backup
	Connected to backup.
	sftp> dir
	SETEST-2016-06    SETEST-weekday-4
	sftp> ls -l */*
	-rw-r--r--    0 1120     1122       199611 Jun  1 20:52 SETEST-weekday-4/geoserver_data_init.tar.gz
	-rw-r--r--    0 1120     1122        16345 Jun  2 00:00 SETEST-weekday-4/backup.log
	-rw-r--r--    0 1120     1122       262846 Jun  2 16:39 SETEST-weekday-4/geoserver_data.tar.gz
	-rw-r--r--    0 1120     1122          542 Jun  2 16:39 SETEST-weekday-4/postgres.sql.bz2
	-rw-r--r--    0 1120     1122          308 Jun  2 16:39 SETEST-weekday-4/backup_db.log
	-rw-r--r--    0 1120     1122        13570 Jun  2 16:39 SETEST-weekday-4/gis.sql.bz2
	-rw-r--r--    0 1120     1122       199611 Jun  1 20:52 SETEST-2016-06/geoserver_data_init.tar.gz
	-rw-r--r--    0 1120     1122        16345 Jun  2 00:00 SETEST-2016-06/backup.log
	-rw-r--r--    0 1120     1122       262846 Jun  2 16:39 SETEST-2016-06/geoserver_data.tar.gz
	-rw-r--r--    0 1120     1122          542 Jun  2 16:39 SETEST-2016-06/postgres.sql.bz2
	-rw-r--r--    0 1120     1122          308 Jun  2 16:39 SETEST-2016-06/backup_db.log
	-rw-r--r--    0 1120     1122        13570 Jun  2 16:39 SETEST-2016-06/gis.sql.bz2


Restoring
=========

To restore, when e.g. the /var/smartem dir is inadvertently deleted (as has happened once), the
entire data and services can be restored in minutes. Only all logging info cannot be restored.
Also handy when moving data to another server.

Latest nightly backups should be under ``/var/smartem/backup``, in worser cases under the ``vps backup``
(see above).

Stop the Platform
-----------------

Be sure to have no ETL nor services running. ::

	service smartem stop

Restore Databases
-----------------

PostGIS and InfluxDB can be restored as follows. ::

	# Be sure to have no dangling data (dangerous!)
	/bin/rm -rf /var/smartem/data/postgresql   # contains all PG data

	# Restart PostGIS: this recreates  /var/smartem/data/postgresql
	~/git/services/postgis/run.sh

	# creeer database schema's globale vars etc
	cd ~/git/platform
	./init-databases.sh

	# Restore PostGIS data for each PG DB schema
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_rt.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_refined.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_calibrated.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_extract.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_harvest-rivm.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-sos52n1.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_raw.dmp    # big one

	# Restore InfluxDB data
    cd /var/smartem/data
    tar xzvf ../backup/influxdb_data.tar.gz


Restore Services
----------------

Services are restored as follows: ::

    # Restore GeoServer data/config
    cd /var/smartem/data
    tar xzvf ../backup/geoserver_data.tar.gz

    # Restore SOS 52North config
    cd /var/smartem/data
    tar xzvf ../backup/sos52n_data.tar.gz

    # Restore Grafana  NOT REQUIRED (config from GitHub)
    # cd /var/smartem/config
    # tar xzvf ../backup/grafana_config.tar.gz

	# Grafana restore (tricky)
	rm -rf /var/smartem/config/grafana
	rm -rf /var/smartem/data/grafana
	rm -rf /var/smartem/log/grafana

	# run once
	cd ~/git/service/grafana
	./run.sh

	# creates all grafana dirs

	# Stop and copy Grafana db (users, dashboards etc.)
	docker stop grafana
	docker rm grafana
	cp /var/smartem/backup/grafana.db  /var/smartem/data/grafana
	./run.sh

	# Check restores via the viewers: smartApp, Heron and SOS Viewer

Restore Calibration Images
--------------------------

Calibration Images can be restored as follows. ::

    cd /opt/geonovum/smartem/git/etl
    tar xzvf /var/smartem/backup/calibration_images.tar.gz


ETL and Data Management
=======================

Republish Data to SOS and STA
-----------------------------

In cases where for example calibration has changed, we need to republish all (refined)
data to the SOS and STA. This is not required for data in GeoServer since it directly
uses the Refined DB tables. SOS and STA keep their own (PostGIS) databases, hence these must be refilled.

Below the steps to republish to SOS and STA, many are common. This should be performed on SE TEST Server: ::

	# stop entire platform: services and cronjobs
    service smartem stop

    # Start PostGIS
    cd ~/git/services/postgis
    ./run.sh

Next do STA and/or SOS specific initializations.

SensorUp STA Specific
~~~~~~~~~~~~~~~~~~~~~

This is specific to STA server from SensorUp. ::

	# use screen as processes may take long
	screen -S sta

    # STA clear data
    cd ~/git/etl/db
    ./staclear.sh
    
    # if this does not work re-init on server
    login at sta.smartemission.nl
    service tomcat8 stop
    su - postgres
    cat db-sensorthings-init.sql | psql sensorthings
    service tomcat8 start
    logout

	# STA Publisher: restart
	./sta-publisher-init.sh

	# STA Test if publishing works again
	cd ~/git/etl
	./stapublisher.sh

	# If ok, reconfigure stapublisher such that it runs forever
	# until no more refined data avail
	# edit stapublisher.cfg such that 'read_once' is False
	# [input_refined_ts_db]
	# class = smartemdb.RefinedDbInput
	# .
	# .
	# read_once = False

	# Now run stapublisher again (will take many hours...)
	./stapublisher.sh

	# Detach screen
	control-A D

52North SOS Specific
~~~~~~~~~~~~~~~~~~~~

This is specific to SOS server from 52North. ::

    # Start SOS
    cd ~/git/services/sos52n
    ./run.sh
    
    # SOS clear DB and other data
    cd ~/git/services/sos52n/config
    ./sos-clear.sh

	# SOS Publisher: restart
    cd ~/git/etl/db
	./sos-publisher-init.sh

	# SOS Test if publishing works again
	cd ~/git/etl
	./sospublisher.sh

	# If ok, reconfigure sospublisher such that it runs forever
	# until no more refined data avail
	# edit sospublisher.cfg such that 'read_once' is False
	# [input_refined_ts_db]
	# class = smartemdb.RefinedDbInput
	# .
	# .
	# read_once = False

	# use screen as processes may take long
	screen -S sos

	# Now run sospublisher again (will take many hours...)
	./sospublisher.sh

	# Detach screen
	control-A D


All dynamic data can be found under ``/var/smartem/data``.

Calibration Model
-----------------

This needs to be intalled from time to time on the production server.
Two parts are incolved: database schema (the model) and images (the results/stats).

All can be restored as follows, assuming we have the data in some backup. ::

	~/git/platform/restore-db.sh gis-smartem_calibrated.dmp
    cd /opt/geonovum/smartem/git/etl
    tar xzvf calibration_images.tar.gz

Web Services
============

TBS

Monitoring
==========

Services Uptime
---------------

All SE API services (WMS, WFS, SOS, STA etc)
and external APIs (Whale Server, Intemo Harvester) are monitored via UptimeRobot.com.

Systems Monitoring
------------------

All systems (Ubuntu OS, Docker etc) are monitored using `Prometheus <https://prometheus.io>`_
with `Exporters <https://prometheus.io/docs/instrumenting/exporters/>`_
and `Grafana <https://grafana.com/>`_.

Prometheus collects and stores data as timeseries by pulling metrics from Exporters. An Exporter collects local
metric data and exposes these via a uniform HTTP API through which Prometheus pulls.
Each Exporter is resource-specific: e.g. a `Node Exporter <https://github.com/prometheus/node_exporter>`_
collects metrics from a Linux OS. Google `cAdvisor <https://github.com/google/cadvisor>`_  will be used
to collect and expose Docker metrics.

Grafana uses Prometheus as a Data source, providing various standard Dashboards for visualization. Also Alerting
can be configured via Prometheus, using the `AlertManager <https://prometheus.io/docs/alerting/alertmanager/>`_
to send to various alerting destinations (email, SMS, webhook etc).

A complete setup for the above can be found at https://github.com/vegasbrianc/prometheus.

Links
~~~~~

Tutorials

* https://www.digitalocean.com/community/tutorials/how-to-install-prometheus-using-docker-on-ubuntu-14-04
* https://www.digitalocean.com/community/tutorials/how-to-use-prometheus-to-monitor-your-ubuntu-14-04-server

* http://phillbarber.blogspot.nl/2015/02/connect-docker-to-service-on-parent-host.html
* https://grafana.com/dashboards/1860
* https://github.com/google/cadvisor

Troubleshooting
===============

Various issues found and their solutions.

Docker won't start
------------------

This may happen after a Ubuntu (kernel) upgrade.
In syslog *"[graphdriver] prior storage driver \"aufs\" failed: driver not supported"*.

* Solution: https://github.com/docker/docker/issues/14026 : Remove dir ``/var/lib/docker/aufs``.

