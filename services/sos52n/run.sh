#!/bin/bash
#
# Run the Postgresql server with PostGIS and default database "gis".
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
NAME="sos52n"
IMAGE="geonovum/sos52n"

# VOL_MAP="-v /var/smartem/data/postgresql:/var/lib/postgresql -v ${LOG}/postgresql:/var/log/postgresql"
# PORT_MAP="-p 5432:5432"
PORT_MAP=""

# Stop and remove possibly old containers
# sudo docker stop ${NAME} > /dev/null 2>&1
# sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
# sudo docker run --name ${NAME} ${PORT_MAP} ${VOL_MAP} -d -t ${IMAGE}

