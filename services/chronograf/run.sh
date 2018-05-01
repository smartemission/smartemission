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

DATA_DIR="/var/smartem/data/chronograf"
mkdir -p ${DATA_DIR}

# EXTRA_ARGS="--bolt-path=/var/lib/chronograf/chronograf.db --basepath=/adm/chronograf --influxdb-url=http://influxdb:8086 --influxdb-username=${influx_admin_user} --influxdb-password=${influx_admin_password}"

export influx_admin_user
export influx_admin_password
echo ${influx_admin_user}

docker-compose rm --force --stop
docker-compose up -d

# sudo docker logs --follow chronograf
