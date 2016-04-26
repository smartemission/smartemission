#!/bin/bash
#
# Run the Apache2 webserver with mapping to local config
#

GIT="/opt/geonovum/smartem/git"
CONFIG="${GIT}/services/web"
LOG="/var/smartem/log"
NAME="web"
IMAGE="geonovum/apache2"

VOL_MAP="-v ${CONFIG}/sites-enabled:/etc/apache2/sites-enabled -v ${GIT}:${GIT} -v ${LOG}/apache2:/var/log/apache2"
PORT_MAP="-p 2222:22 -p 80:80"
LINK_MAP="--link ${PG_HOST}:${PG_HOST}"
PG_HOST="postgis"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
sudo docker run -d --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -t -i ${IMAGE}
