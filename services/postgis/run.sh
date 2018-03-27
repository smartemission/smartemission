#!/bin/bash
#
# Run the Postgresql server with PostGIS and default database "gis".
#

# Stop and remove possibly old containers
docker-compose stop
docker-compose rm -f

# Finally run
# sudo docker run --restart=always --name ${NAME} ${PORT_MAP} ${VOL_MAP} -d -t ${IMAGE}
docker-compose up -d

# TIP to connect from host to postgis container
# psql -h `sudo docker inspect --format '{{ .NetworkSettings.Networks.se_back.IPAddress }}' postgis` -U docker -W gis
