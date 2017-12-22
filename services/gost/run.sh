#!/bin/bash
#
# Run the SensorThings API (STA) GOST server with mapping to local config
# Docker image: https://hub.docker.com/r/geodan/gost/
#

#GIT="/opt/geonovum/smartem/git"

# Get Settings from local options file
source ../../etl/options/`hostname`.args

# Later: docker compose: too much hassle now...
#export gost_server_external_uri
#docker-compose up

ENV_MAP="-e gost_server_external_uri=${gost_server_external_uri} -e gost_mqtt_host=mosquitto"
LOG="/var/smartem/log"
NAME="gost"
IMAGE="geodan/gost:0.5"
PG_HOST="postgis"
MOSQUITTO_HOST="mosquitto"

# Define Volume mappings, map local config file
VOL_MAP="-v ${PWD}/config/config.yaml:/go/bin/gost/config.yaml"

# If we need to expose 8080 from host
#PORT_MAP="-p 8080:8080"
PORT_MAP=""
#
LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${MOSQUITTO_HOST}:${MOSQUITTO_HOST}"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1
sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} ${ENV_MAP} -d ${IMAGE}

# sudo docker logs --follow gost
