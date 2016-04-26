#!/bin/bash
#
# Run the Postgresql server with PostGIS and default database "gis".
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
NAME="geoserver"
IMAGE="kartoza/geoserver:2.8.0"
IMAGE="geonovum/geoserver"
PG_HOST="postgis"
DATA_DIR="/var/smartem/data/geoserver"
if [ ! -d ${DATA_DIR} ]
then
 sudo mkdir -p ${DATA_DIR}
fi

VOL_MAP="-v ${DATA_DIR}:/opt/geoserver/data_dir"
PORT_MAP="-p 8080:8080"
LINK_MAP="--link ${PG_HOST}:${PG_HOST}"

# Stop and remove possibly old containers
sudo docker kill ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
sudo docker run --name ${NAME} ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}
