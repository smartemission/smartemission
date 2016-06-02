.. _admin:

==============
Administration
==============

This chapter describes the operation and maintenance aspects for the Smart Emission platform. For example:

* how to start stop servers
* managing the ETL
* where to find logfiles
* troubleshooting

Platform Overall
================

To install the entire platform and run it as a system service.
From the ``GIT_HOME/platform`` dir do:

* ``./bootstrap.sh`` - makes empty Ubuntu system ready for Docker and Platform
* ``./build.sh``  - builds all Docker images
* ``./install.sh``  - installs system service "smartem"

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
In syslog ``"[graphdriver] prior storage driver \"aufs\" failed: driver not supported" ``.

* Solution: https://github.com/docker/docker/issues/14026 : Remove dir ``/var/lib/docker/aufs``.

