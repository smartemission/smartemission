#!/bin/bash
#
# Run the GeoServer Docker image with local and PostGIS Docker mappings.
#

#GIT="/opt/geonovum/smartem/git"
#LOG="/var/smartem/log"
#TC_LOG="${LOG}/tomcat-geoserver"
#NAME="geoserver"
#IMAGE="geonovum/geoserver:2.9.0"
#PG_HOST="postgis"
#DATA_DIR="/var/smartem/data"
#GS_DATA_DIR="${DATA_DIR}/geoserver"
#
## Define the mappings for local dirs, ports and PostGIS Docker container
#VOL_MAP_DATA="-v ${GS_DATA_DIR}:/opt/geoserver/data_dir"
#VOL_MAP_LOGS="-v ${TC_LOG}:/usr/local/tomcat/logs"
#VOL_MAP_FULL="${VOL_MAP_DATA} ${VOL_MAP_LOGS}"
#
## If we need to expose 8080 from host, but we use Apache AJP
## PORT_MAP="-p 8080:8080"
#PORT_MAP=""
## LINK_MAP="--link ${PG_HOST}:${PG_HOST}"
#
## Restart with volume mapping(s) provided in $1
#function restart_gs() {
#  VOL_MAP="$@"
#
#  # Stop and remove possibly old containers
#  sudo docker stop ${NAME} > /dev/null 2>&1
#  sudo docker rm ${NAME} > /dev/null 2>&1
#  echo "restart ${NAME} with volumes: ${VOL_MAP}"
#  # Finally run with all mappings
#  sudo docker run --restart=unless-stopped --name ${NAME} --network="se_back" ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}
#}
#
## Some tricky stuff to get full GS data dir on host when non-existing on host
#if [ ! -d "${GS_DATA_DIR}" ]; then
#   # First time: get full GS data dir. Loosing/rebuilding the Docker image will thus
#   # never result in loss of data.
#   # For GeoServer we  need to copy the original data dir from the container
#   # to the host on first run.
#   # See issue: https://github.com/kartoza/docker-geoserver/issues/2
#   # (not an issue anymore, see comments there)
#   echo "${GS_DATA_DIR} empty: copy from original GS version and restart GS"
#   restart_gs ${VOL_MAP_LOGS}
#
#   # Copy from original data dir in container and rename by moving on host
#   sudo docker cp geoserver:/opt/geoserver/data_dir $DATA_DIR
#   sudo rm -rf ${GS_DATA_DIR}
#   sudo mv  ${DATA_DIR}/data_dir ${GS_DATA_DIR}
#   sudo rm -rf ${TC_LOG}
#
#   # Rerun with full volume mapping
#   restart_gs ${VOL_MAP_FULL}
#else
#   echo "Ok, using existing GeoServer data dir: ${GS_DATA_DIR} on host"
#   restart_gs ${VOL_MAP_FULL}
#fi

# Need HOSTNAME within docker-compose for host-specific path to env file.
export HOSTNAME

docker-compose rm --force --stop
docker-compose up -d

# When running: get into container with bash
# sudo docker exec -it geoserver  bash
