#!/bin/bash
#
# Run the Apache2 webserver with mapping to local config
#

SCRIPT_DIR=${0%/*}
pushd ${SCRIPT_DIR}
SCRIPT_DIR=$PWD
popd

LOG="/var/smartem/log"
BACKUP="/var/smartem/backup"

# In order to have proxy access node_exporter metrics for Prometheus
# See http://phillbarber.blogspot.nl/2015/02/connect-docker-to-service-on-parent-host.html
PARENT_HOST=`ip route show | grep docker0 | awk '{print \$9}'`
HOSTS_MAP="--add-host=parent-host:${PARENT_HOST}"

# Somehow needed for mounts
chmod 777 ${LOG} ${BACKUP} ${SCRIPT_DIR}/../../etl/calibration

# Stop and remove possibly old containers
docker-compose stop
docker-compose rm -f

# Finally run
docker-compose up -d
