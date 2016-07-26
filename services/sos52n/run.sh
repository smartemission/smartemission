#!/bin/bash
#
# Run the 52NorthSOS Docker image with local and PostGIS Docker mappings.
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
TC_LOG="${LOG}/tomcat-sos52n"
NAME="sos52n"
IMAGE="geonovum/sos52n:4.3.7"
PG_HOST="postgis"
IMAGE_TC_DIR=/usr/local/tomcat
DATA_DIR="/var/smartem/data"
SOS_DATA_DIR="${DATA_DIR}/sos52n"

# Define the mappings for local dirs, ports and PostGIS Docker container
# VOL_MAP_DATA="-v ${SOS_DATA_DIR}:/opt/sos52n/data_dir"
VOL_MAP_MIN="-v ${TC_LOG}:${IMAGE_TC_DIR}/logs"
VOL_MAP_FULL="-v ${SOS_DATA_DIR}:/opt/sosconfig ${VOL_MAP_MIN}"

# If we need to expose 8080 from host, but we use Apache AJP
# PORT_MAP="-p 8080:8080"
PORT_MAP=""
LINK_MAP="--link ${PG_HOST}:${PG_HOST}"

# When running: get into container with bash
# sudo docker exec -it sos52n  bash

# Restart with volume mapping(s) provided in $1
function restart_image() {
  VOL_MAP="$@"

  # Stop and remove possibly old containers
  sudo docker stop ${NAME} > /dev/null 2>&1
  sudo docker rm ${NAME} > /dev/null 2>&1
  echo "restart ${NAME} with volumes: ${VOL_MAP}"
  
  # Finally run with all mappings
  sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}
  sudo docker cp config/jsclient/settings.json sos52n:/usr/local/tomcat/webapps/sos52n/static/client/jsClient
}

# Some tricky stuff to get full SOS data dir on host when non-existing on host
if [ ! -d "${SOS_DATA_DIR}" ]; then
   # First time: get SOS data dir (configuration.db). 
   # Loosing/rebuilding the Docker image will thus
   # never result in loss of config data, plus we can maintain it on the host.
   # For 52NorthSOS we need to copy the original data dir from the container
   # to the host on first run.
   echo "${SOS_DATA_DIR} empty: copy from original SOS version and restart SOS"
   restart_image ${VOL_MAP_MIN}

   # Copy from original data dir in container and rename by moving on host
   sudo docker cp sos52n:/opt/sosconfig ${SOS_DATA_DIR}
   sudo rm -rf ${TC_LOG}

   # Rerun with full volume mapping
   restart_image ${VOL_MAP_FULL}

   echo "THIS IS THE FIRST RUN WITH DEFAULT configuration.db - CHANGE YOUR SOS-PASSWORD"
else
   echo "Ok, using existing 52NorthSOS data dir: $SOS_DATA_DIR on host"
   restart_image ${VOL_MAP_FULL}
fi
