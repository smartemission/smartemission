#!/bin/bash
#
# Run the Postgresql server with PostGIS and default database "gis".
#

#GIT="/opt/geonovum/smartem/git"
#SCRIPT_DIR=${GIT}/services/postgis
#LOG="/var/smartem/log"
#NAME="postgis"
## IMAGE="kartoza/postgis:9.4-2.1"
#IMAGE="geonovum/postgis:9.4-2.1"
#PG_CONF_DIR=/var/smartem/data/postgresql/9.4/main

# If PG dir on host copy config file
#if [ -d "${PG_CONF_DIR}" ]
#then
#  echo "Copy postgresql.conf to ${PG_CONF_DIR}"
#  sudo cp ${SCRIPT_DIR}/config/postgresql.conf ${PG_CONF_DIR}
#  # sudo cp ${SCRIPT_DIR}/config/pg_hba.conf ${PG_CONF_DIR}
#fi
#
#VOL_MAP="-v /var/smartem/data/postgresql:/var/lib/postgresql -v ${LOG}/postgresql:/var/log/postgresql -v /var/smartem/backup:/var/smartem/backup"
#
#PORT_MAP="-p 5432:5432"
# PG not accessible from outside!
# PORT_MAP=""

# Stop and remove possibly old containers
docker-compose stop
docker-compose rm

# Finally run
# sudo docker run --restart=always --name ${NAME} ${PORT_MAP} ${VOL_MAP} -d -t ${IMAGE}
docker-compose up -d

# TIP to connect from host to postgis container
# psql -h `sudo docker inspect --format '{{ .NetworkSettings.Networks.se_back.IPAddress }}' postgis` -U docker -W gis
