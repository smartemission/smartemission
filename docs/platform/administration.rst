.. _admin:

==============
Administration
==============

This chapter describes the operation and maintenance aspects for the Smart Emission platform. For example:

* installing/setting up the entire platform
* how to start stop servers
* managing the ETL
* where to find logfiles
* troubleshooting

Platform Overall
================

To install the entire platform on Ubuntu Linux on an empty Virtual Machine (VM)
make all databases ready and run it as a system service.
From the ``GIT_HOME/platform`` dir do:

* ``sudo su -`` - become root
* ``./bootstrap.sh`` - makes empty Ubuntu system ready for Docker and Platform
* ``./build.sh``  - builds all Docker images (be patient)
* ``init-databases.sh`` - creates and initializes all databases (**NB WILL DESTROY ANY EXISTING DATA!**)
* ``./install.sh``  - installs system service "smartem" in ``/etc/init.d``

For the ``init-databases.sh`` script you need to add a file ``<myhostname>.args`` under ``etl/options`` similar
to ``example.args`` where ``<myhostname>`` is the result of the ``hostname`` command.

Now use the standard Linux "service" commands:  ::

	service smartem status
	service smarted stop
	service smartem start

etc or even ``/etc/init.d/smartem start|stop|status`` will work.

The link http://data.smartemission.nl/adm gives access to admin pages.

Checking status: ::

	$ service smartem status
	 * Checking status of Smart Emission Data Platform smartem                                                                                                                             CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                        NAMES
	8e4e7610f81e        geonovum/apache2           "/usr/bin/supervisord"   10 minutes ago      Up 10 minutes       22/tcp, 0.0.0.0:80->80/tcp   web
	12caa42044a8        geonovum/geoserver:2.9.0   "catalina.sh run"        10 minutes ago      Up 10 minutes       8080/tcp                     geoserver
	af79831923a3        geonovum/postgis           "/bin/sh -c /start-po"   11 minutes ago      Up 10 minutes       5432/tcp                     postgis


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

Latest nightly backups should be under ``/var/smartem/backup``, in worser cases under the ``vps backup`` (see above).

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

	# Restore PostGIS data for each PG DB schema
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_rt.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_refined.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_extract.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_harvest-rivm.dmp
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-smartem_raw.dmp    # big one
    ~/git/platform/restore-db.sh /var/smartem/backup/gis-sos52n1.dmp

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

    # Check restores via the viewers: smartApp, Heron and SOS Viewer

	# TODO Grafana

Data Management
===============

All dynamic data can be found under ``/var/smartem/data``.

Web Services
============

TBS

Troubleshooting
===============

Various issues found and their solutions.

Docker won't start
------------------

This may happen after a Ubuntu (kernel) upgrade.
In syslog *"[graphdriver] prior storage driver \"aufs\" failed: driver not supported"*.

* Solution: https://github.com/docker/docker/issues/14026 : Remove dir ``/var/lib/docker/aufs``.

