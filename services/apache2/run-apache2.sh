#!/bin/bash
#
# Run the Apache2 server with mapping to local config
#

GIT="/opt/geonovum/smartem/git"
WWW="${GIT}/www"
CONFIG="${GIT}/services/apache2"
LOG="/var/smartem/log"
NAME="apache2"
IMAGE="geonovum/apache2"

VOL_MAP="-v ${CONFIG}/sites-enabled:/etc/apache2/sites-enabled -v ${GIT}:${GIT} -v ${LOG}/apache2:/var/log/apache2"
PORT_MAP="-p 2222:22 -p 80:80"
PG_HOST="postgis"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
sudo docker run --name ${NAME} --link ${PG_HOST}:${PG_HOST} -d ${PORT_MAP} ${VOL_MAP} -t -i ${IMAGE}
