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

TBS

SOS Services
============

*"The OGC Sensor Observation Service aggregates readings from live, in-situ and remote sensors.*
*The service provides an interface to make sensors and sensor data archives accessible via an*
*interoperable web based interface."*

The chapter on server administration describes how the SOS is deployed. This is
called here the 'SOS Server'.

istSOS - Install Test
---------------------

Notes from raw install as Python WSGI app, see also http://istsos.org/en/latest/doc/installation.html:  ::

	# as root
	$ mkdir /opt/istsos
	$ cd /opt/istsos
	# NB 2.3.0 gave problems, see https://sourceforge.net/p/istsos/tickets/41/
	$ wget https://sourceforge.net/projects/istsos/files/istsos-2.3.0.tar.gz
	$ tar xzvf istsos-2.3.0.tar.gz
	$ mv istsos 2.3.0
	$ ln -s 2.3.0 latest

	$ chmod 755 -R /opt/istsos/latest
	$ chown -R www-data:www-data /opt/istsos/latest/services
	$ chown -R www-data:www-data /opt/istsos/latest/logs
	$ mkdir /opt/istsos/latest/wns   # not present, need to create, no is for web notification service
	$ chown -R www-data:www-data /opt/istsos/latest/wns # not present, gives error (?)

Add WSGI app to Apache conf.

.. literalinclude:: ../../services/web/config/sites-enabled/000-default.conf
    :language: text

Setup the PostGIS database. ::

	$ sudo su - postgres
    $ createdb -E UTF8 -O sensors istsos
    Password:
    $ psql -d istsos -c 'CREATE EXTENSION postgis'
    Password:
    CREATE EXTENSION

Restart and test: ::

	$ service apache2 restart

	# in browser
	http://api.smartemission.nl/istsos/admin/

	# Database: fill in user/password

	# create service (creates DB schema) "sound"

    # test requests
    http://api.smartemission.nl/istsos/modules/requests/

    # REST
    http://api.smartemission.nl/istsos/wa/istsos/services/sound





