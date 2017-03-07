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

