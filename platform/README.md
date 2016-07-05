# Smart Emission Data Platform

Global resources (scripts, cron, backup etc) to bootstrap, build, run and maintain the 
entire Smart Emission Data Platform.

Documentation for the Smartemission Data Platform can be found at: http://smartplatform.readthedocs.org

On a clean Ubuntu system the whole platform can be up and running within 15 minutes.
The entire platform will run as a System service from /etc/init.d/smartem thus surviving reboots.

"Running" the Platform entails running the Docker images, scheduling regular tasks (cron) for ETL and backup.
All is controlled using the systemd standard Linux service "smartem".

## Installation

From this dir do as `root`:

    ./bootstrap.sh - makes empty Ubuntu system ready for Docker and Platform
    ./build.sh  - builds all Docker images
    ./install.sh  - installs system service "smartem"

Then use the standard Linux "service" commands:

    service smartem status
    service smarted stop
    service smartem start
    etc

Also `/etc/init.d/smartem start| stop | status` should work.

Databases (3) need to be initialized once in order to facilitate ETL (NB the `postgis` Docker container needs to be running!)

	cd ../etl/db
	./db-init-last.sh
	./db-init-raw.sh
	./db-init-refined.sh
	
	# test ETL using .sh scripts
	./last.sh
	./harvester.sh
	./refiner.sh
		
## Administration

All dynamic data (config, databases, logfiles) is kept outside the Docker images. Most under `/var/smartem`.

An admin web-interface (see `services/web/site/adm`) is present at `/adm`.
Create the file `htpaswd` once under `/opt/geonovum/smartem/git/services/web/config/admin` 
using the command `htpasswd`. You may need to install the package `apache2-utils` first.
