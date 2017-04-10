#!/bin/bash
#
# Run the SensorThings API (STA) GOST server with mapping to local config
# Docker image: https://hub.docker.com/r/geodan/gost/
#

GIT="/opt/geonovum/smartem/git"

# Get Settings from local options file
source ${GIT}/etl/options/`hostname`.args
ENV_MAP="-e gost_server_external_uri=${gost_server_external_uri}"

LOG="/var/smartem/log"
NAME="gost"
IMAGE="geodan/gost:0.4"
PG_HOST="postgis"

# Define Volume mappings, map local config file
VOL_MAP="-v ${GIT}/services/gost/config/config.yaml:/go/bin/gost/config.yaml -v ${GIT}/services/gost/config/app.js:/go/bin/gost/client/js/app.js"

# If we need to expose 8080 from host
PORT_MAP="-p 8080:8080"

LINK_MAP="--link ${PG_HOST}:${PG_HOST}"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1
sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} ${ENV_MAP} -d ${IMAGE}

# sudo docker logs --follow gost
