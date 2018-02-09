#!/bin/bash
#
# Run the SensorThings API (STA) GOST server Dashboard UI
# Docker image: https://store.docker.com/community/images/geodan/gost-dashboard
#

# Get Settings from local options file
source ../../etl/options/`hostname`.args

LOG="/var/smartem/log"
NAME="gostdashboard"
IMAGE="geodan/gost-dashboard-v2:latest"
GOST_HOST=gost

# Define Volume mappings, map local config file
VOL_MAP="-v ${PWD}/config/client_config.json:/var/www/html/client_config.json"

# Temporary overrides until this issue is fixed:
# https://github.com/Geonovum/smartemission/issues/81
OVERRIDE_VOL_MAP="-v ${PWD}/overrides/seed-app.html:/var/www/html/elements/seed-app/seed-app.html -v ${PWD}/overrides/index.html:/var/www/html/index.html"

# If we need to expose 8080 from host
PORT_MAP="-p 8083:8080"
PORT_MAP=""

#
LINK_MAP="--link ${GOST_HOST}:${GOST_HOST}"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1
sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} ${OVERRIDE_VOL_MAP} -d ${IMAGE}

# docker logs --follow gostdashboard
