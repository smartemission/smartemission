#!/bin/bash
#
# Run Grafana from http://docs.grafana.org/installation/docker/
#
# On first run the config, data and log dirs are copied from container to /var/smartem/* dirs.
# InfluxDB needs to run first.
# NB Change the default password there!

GIT="/opt/geonovum/smartem/git"
LOG_DIR="/var/smartem/log/grafana"
DATA_DIR="/var/smartem/data/grafana"
CONFIG_DIR="/var/smartem/config/grafana"
NAME="grafana"
IMAGE="grafana/grafana:develop"
INFLUX_HOST=influxdb

# Volume maps for initial and full run
VOL_MAP_PART=" "
VOL_MAP_FULL="-v ${DATA_DIR}/grafana:/var/lib/grafana -v ${LOG_DIR}/grafana:/var/log/grafana -v ${CONFIG_DIR}/grafana:/etc/grafana"

PORT_MAP="-p 3000:3000"
LINK_MAP="--link ${INFLUX_HOST}:${INFLUX_HOST}"

# Restart with volume mapping(s) provided in $1
function restart_image() {
  VOL_MAP="$@"

  # Stop and remove possibly old containers
  sudo docker stop ${NAME} > /dev/null 2>&1
  sudo docker rm ${NAME} > /dev/null 2>&1
  echo "restart ${NAME} with volumes: ${VOL_MAP}"
  # Finally run with all mappings
  sudo docker run --name ${NAME} ${PORT_MAP} ${VOL_MAP} ${LINK_MAP} -d ${IMAGE}
}

# Some tricky stuff to get all Grafana dirs on host when non-existing on host
if [ ! -d "${CONFIG_DIR}" ]; then
   # First time: get Grafana dirs. Loosing/rebuilding the Docker image will thus
   # never result in loss of data.
   # to the host on first run.
   # In subsequent runs we can adapt the config etc. The data is also saved outside container.
   echo "${CONFIG_DIR} empty: copy from original ${NAME} version to ${CONFIG_DIR}"
   restart_image ${VOL_MAP_PART}

   # Copy from original data dir in container and rename by moving on host
   sudo rm -rf ${DATA_DIR}
   sudo rm -rf ${LOG_DIR}
   sudo mkdir -p ${CONFIG_DIR}
   sudo mkdir -p ${DATA_DIR}
   sudo mkdir -p ${LOG_DIR}
   sudo docker cp ${NAME}:/etc/grafana ${CONFIG_DIR}
   sudo docker cp ${NAME}:/var/lib/grafana ${DATA_DIR}
   sudo docker cp ${NAME}:/var/log/grafana ${LOG_DIR}

   # Rerun with full volume mapping
   restart_image ${VOL_MAP_FULL}
else
   echo "Ok, using existing ${CONFIG_DIR} dir on host"
   restart_image ${VOL_MAP_FULL}
fi
