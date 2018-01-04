#!/bin/bash
#
# Run the chronograf with mapping to local config.
# See https://docs.influxdata.com/chronograf/v1.3/
# Docker image: https://hub.docker.com/_/chronograf/
# GitHub: https://github.com/toke/docker-chronograf
#

SCRIPT_DIR=${0%/*}
pushd ${SCRIPT_DIR}
  SCRIPT_DIR=$PWD
popd

source ${SCRIPT_DIR}/../../etl/options/`hostname`.args

CONFIG_DIR="${SCRIPT_DIR}/config"
DATA_DIR="/var/smartem/data/chronograf"
LOG_DIR="/var/smartem/log/chronograf"
INFLUX_HOST=influxdb

# Optional dir create
sudo mkdir -p ${DATA_DIR}
sudo mkdir -p ${LOG_DIR}
sudo chmod 777 ${LOG_DIR}

NAME="chronograf"
IMAGE="chronograf:1.4-alpine"

# Define Volume mappings, map local config file
# See https://github.com/toke/docker-chronograf/blob/master/README.md
VOL_MAP="-v ${DATA_DIR}:/var/lib/chronograf"

# If we need to expose host
PORT_MAP="-p 8888:8888"

LINK_MAP="--link ${INFLUX_HOST}:${INFLUX_HOST}"

EXTRA_ARGS="--bolt-path=/var/lib/chronograf/chronograf.db --basepath=/adm/chronograf --influxdb-url=http://influxdb:8086 --influxdb-username=${influx_admin_user} --influxdb-password=${influx_admin_password}"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1
sudo docker run --name ${NAME} ${PORT_MAP} ${VOL_MAP} ${LINK_MAP} -d ${IMAGE} ${EXTRA_ARGS}

# sudo docker logs --follow chronograf
