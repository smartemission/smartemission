#!/bin/bash
#
# Run the GeoServer Docker image with local and PostGIS Docker mappings.
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
TC_LOG="${LOG}/tomcat-geoserver"
NAME="geoserver"
# IMAGE="kartoza/geoserver:2.8.0"
IMAGE="geonovum/geoserver:2.9.0"
PG_HOST="postgis"
DATA_DIR="/var/smartem/data"
GS_DATA_DIR="${DATA_DIR}/geoserver"

# First time: may make emtpy dirs. Docker will fill these once with
# values in container and leave them in subsequent runs. Hence the GeoServer
# data dir can be maintained on the host. Loosing/rebuilding the Docker image will thus
# never result in loss of data.

# sudo mkdir -p ${DATA_DIR}
# sudo mkdir -p ${TC_LOG}

# Define the mappings for local dirs, ports and PostGIS Docker container
VOL_MAP="-v ${GS_DATA_DIR}:/opt/geoserver/data_dir -v ${TC_LOG}:/usr/local/tomcat/logs"

# PORT_MAP="-p 8080:8080"
PORT_MAP=""
LINK_MAP="--link ${PG_HOST}:${PG_HOST}"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run with all mappings
sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}

if [ "$(ls -A $GS_DATA_DIR)" ]; then
   echo "Ok, using existing GeoServer data dir: $GS_DATA_DIR on host"
else
   echo "$GS_DATA_DIR empty: copy from original GS version and restart GS"
   # Copy from original (somehow mapping render an empty dir!)
   sudo docker cp geoserver:/opt/geoserver/data_dir.orig $DATA_DIR
   sudo rm -rf $GS_DATA_DIR
   sudo mv  ${DATA_DIR}/data_dir.orig $GS_DATA_DIR

   # Rerun
   sudo docker stop ${NAME} > /dev/null 2>&1
   sudo docker rm ${NAME} > /dev/null 2>&1
   sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}
fi

# When running: get into container with bash
# sudo docker exec -it geoserver  bash
