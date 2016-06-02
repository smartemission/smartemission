#!/bin/bash
#
# Stop all services (Docker Containers)

# CONTAINERS="web geoserver sos52n postgis"
CONTAINERS="web geoserver postgis"
for CONTAINER in ${CONTAINERS}
do
  echo "stopping ${CONTAINER}"
  sudo docker stop ${CONTAINER}
done
