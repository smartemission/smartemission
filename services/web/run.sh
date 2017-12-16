#!/bin/bash
#
# Run the Apache2 webserver with mapping to local config
#

GIT="/opt/geonovum/smartem/git"
CONFIG="${GIT}/services/web/config"
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
PROMETHEUS_HOST="prometheus"

# In order to have proxy access node_exporter metrics for Prometheus
# See http://phillbarber.blogspot.nl/2015/02/connect-docker-to-service-on-parent-host.html
PARENT_HOST=`ip route show | grep docker0 | awk '{print \$9}'`

# Somehow needed for mounts
sudo chmod 777 ${LOG} ${BACKUP} ${GIT}/etl/calibration

VOL_MAP="-v ${CONFIG}/admin:/etc/apache2/admin -v ${CONFIG}/phppgadmin:/etc/phppgadmin -v ${CONFIG}/sites-enabled:/etc/apache2/sites-enabled -v ${GIT}:${GIT} -v ${LOG}/apache2:/var/log/apache2 -v ${LOG}:/smartemlogs -v ${BACKUP}:/smartembackups"
PORT_MAP="-p 80:80"
LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${GS_HOST}:${GS_HOST} --link ${SOS52N_HOST}:${SOS52N_HOST} --link ${INFLUXDB_HOST}:${INFLUXDB_HOST} --link ${GRAFANA_HOST}:${GRAFANA_HOST} --link ${STA_GOST_HOST}:${STA_GOST_HOST} --link ${PROMETHEUS_HOST}:${PROMETHEUS_HOST}"
# LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${STA_GOST_HOST}:${STA_GOST_HOST}"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
sudo docker run -d --restart=always --add-host=parent-host:${PARENT_HOST} --name ${NAME} ${LINK_MAP} ${PORT_MAP} ${VOL_MAP} -t -i ${IMAGE}
