#!/bin/bash
#
# Run the Prometheus server
#
# See https://prometheus.io/docs/prometheus/latest/installation/
SCRIPT_DIR=${0%/*}
pushd ${SCRIPT_DIR}
SCRIPT_DIR=$PWD
popd

source ${SCRIPT_DIR}/../../etl/options/`hostname`.args

LOG_DIR="/var/smartem/log/prometheus"
DATA_DIR="/var/smartem/data/prometheus"
CONFIG_DIR="${SCRIPT_DIR}/config"
NAME="prometheus"
IMAGE="prom/prometheus:master"
mkdir -p ${DATA_DIR}

VOL_MAP="-v ${CONFIG_DIR}:/etc/prometheus -v ${DATA_DIR}:/promdata"
PORT_MAP=""
LINK_MAP=""
OPTIONS="--config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/promdata --web.console.libraries=/usr/share/prometheus/console_libraries --web.console.templates=/usr/share/prometheus/consoles --web.external-url=http://${se_host}/adm/prometheus"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
# docker run -p 9090:9090 -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

echo "Run Prometheus with options: ${OPTIONS}"
docker run -d --restart=always -u root --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -t -i ${IMAGE} ${OPTIONS}
