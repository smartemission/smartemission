#!/bin/bash
#
# Run the 52NorthSOS Docker image with local and PostGIS Docker mappings.
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
TC_LOG="${LOG}/tomcat-sos52n"
NAME="sos52n"
IMAGE="geonovum/sos52n:4.3.6"
PG_HOST="postgis"

# Define the mappings for local dirs, ports and PostGIS Docker container
# VOL_MAP_DATA="-v ${GS_DATA_DIR}:/opt/sos52n/data_dir"
VOL_MAP_LOGS="-v ${TC_LOG}:/usr/local/tomcat/logs"
VOL_MAP="${VOL_MAP_LOGS}"

# If we need to expose 8080 from host, but we use Apache AJP
# PORT_MAP="-p 8080:8080"
PORT_MAP=""
LINK_MAP="--link ${PG_HOST}:${PG_HOST}"

echo "Start ${NAME} with volumes: ${VOL_MAP}"
# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1
# Finally run with all mappings
sudo docker run --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}

# When running: get into container with bash
# sudo docker exec -it sos52n  bash
