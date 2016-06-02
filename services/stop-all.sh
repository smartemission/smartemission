#!/bin/bash
#
# Stop all services (Docker Containers)

CONTAINERS="web geoserver postgis sos52n"
for CONTAINER in ${CONTAINERS}
do
	sudo docker stop ${NAME} > /dev/null 2>&1
done

