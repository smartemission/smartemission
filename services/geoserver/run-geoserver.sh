#!/bin/bash
#
# Run the GeoServer Docker image with local and PostGIS Docker mappings.
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
TC_LOG="${LOG}/tomcat-geoserver"
NAME="geoserver"
# IMAGE="kartoza/geoserver:2.8.0"
IMAGE="geonovum/geoserver"
PG_HOST="postgis"
DATA_DIR="/var/smartem/data/geoserver"

# First time: may make emtpy dirs. Docker will fill these once with
# values in container and leave them in subsequent runs. Hence the GeoServer
# data dir can be maintained on the host. Loosing/rebuilding the Docker image will thus
# never result in loss of data.

sudo mkdir -p ${DATA_DIR}
sudo mkdir -p ${TC_LOG}

# Define the mappings for local dirs, ports and PostGIS Docker container
VOL_MAP="-v ${DATA_DIR}:/opt/geoserver/data_dir -v ${TC_LOG}:/usr/local/tomcat/logs"
# PORT_MAP="-p 8080:8080"
PORT_MAP=""
LINK_MAP="--link ${PG_HOST}:${PG_HOST}"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run with all mappings
sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}

# When running: get into container with bash
# sudo docker exec -it geoserver  bash

