#!/bin/bash
#
# Run the InfluxDB from https://hub.docker.com/_/influxdb/.
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
NAME="influxdb"
IMAGE="influxdb/alpine:1.1"

mkdir -p /var/smartem/data/influxdb

VOL_MAP="-v /var/smartem/data/influxdb:/var/lib/influxdb"
PORT_MAP="-p 8083:8083 -p 8086:8086"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
sudo docker run --name ${NAME} ${PORT_MAP} ${VOL_MAP} -d -t ${IMAGE}

# docker run --rm influxdb influxd config > influxdb.conf