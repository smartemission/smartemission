# Smart Emission Data Platform

Global resources (scripts, cron, backup etc) to bootstrap, build, run and maintain the 
entire Smart Emission Data Platform.

Documentation for the Smartemission Data Platform can be found at: http://smartplatform.readthedocs.org

On a clean Ubuntu system the whole platform can be up and running within 15 minutes.
The entire platform will run as a System service from /etc/init.d/smartem thus surviving reboots.

"Running" the Platform entails running the Docker images, scheduling regular tasks (cron) for ETL and backup.
All is controlled using the systemd standard Linux service "smartem".

## Steps

From this dir do:

    ./bootstrap.sh - makes empty Ubuntu system ready for Docker and Platform
    ./build.sh  - builds all Docker images
    ./install.sh  - installs system service "smartem"

Then use the standard Linux "service" commands:

    service smartem status
    service smarted stop
    service smartem start
    etc

Also /etc/init.d/smartem start| stop | status will work.

