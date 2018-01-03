#!/bin/bash
#
# Run the Apache2 webserver with mapping to local config
#

SCRIPT_DIR=${0%/*}
pushd ${SCRIPT_DIR}
SCRIPT_DIR=$PWD
popd

GIT="/opt/geonovum/smartem/git"
CONFIG="${SCRIPT_DIR}/config"
LOG="/var/smartem/log"
BACKUP="/var/smartem/backup"
NAME="web"
IMAGE="geonovum/apache2"

# backends
PG_HOST="postgis"
GS_HOST="geoserver"
SOS52N_HOST="sos52n"
INFLUXDB_HOST="influxdb"
GRAFANA_HOST="grafana"
STA_GOST_HOST="gost"
STA_GOSTDASHBOARD_HOST="gostdashboard"

# Monitoring
MON_PROMETHEUS_HOST="monitoring_prometheus_1"
MON_GRAFANA_HOST="monitoring_grafana_1"

# In order to have proxy access node_exporter metrics for Prometheus
# See http://phillbarber.blogspot.nl/2015/02/connect-docker-to-service-on-parent-host.html
PARENT_HOST=`ip route show | grep docker0 | awk '{print \$9}'`

# Somehow needed for mounts
sudo chmod 777 ${LOG} ${BACKUP} ${SCRIPT_DIR}/../../etl/calibration

VOL_MAP="-v ${CONFIG}/admin:/etc/apache2/admin -v ${CONFIG}/phppgadmin:/etc/phppgadmin -v ${SCRIPT_DIR}/config/sites-enabled:/etc/apache2/sites-enabled -v ${GIT}:${GIT} -v ${LOG}/apache2:/var/log/apache2 -v ${LOG}:/smartemlogs -v ${BACKUP}:/smartembackups"
PORT_MAP="-p 80:80"

#
LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${GS_HOST}:${GS_HOST} --link ${SOS52N_HOST}:${SOS52N_HOST} --link ${INFLUXDB_HOST}:${INFLUXDB_HOST} --link ${GRAFANA_HOST}:${GRAFANA_HOST} --link ${STA_GOST_HOST}:${STA_GOST_HOST} --link ${STA_GOSTDASHBOARD_HOST}:${STA_GOSTDASHBOARD_HOST} --link ${MON_PROMETHEUS_HOST}:${MON_PROMETHEUS_HOST} --link ${MON_GRAFANA_HOST}:${MON_GRAFANA_HOST}"
# LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${SOS52N_HOST}:${SOS52N_HOST}"
# NETWORKS="--network=monitoring_front-tier"

HOSTS_MAP="--add-host=parent-host:${PARENT_HOST}"
# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
# --add-host=parent-host:${PARENT_HOST} 
sudo docker run -d --restart=always  --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${HOSTS_MAP} ${VOL_MAP} -t -i ${IMAGE}
