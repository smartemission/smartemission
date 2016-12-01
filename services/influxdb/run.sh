#!/bin/bash
#
# Run the InfluxDB from https://hub.docker.com/_/influxdb/.
#

GIT="/opt/geonovum/smartem/git"
LOG="/var/smartem/log"
NAME="influxdb"
IMAGE="influxdb:1.1"

mkdir -p /var/smartem/data/influxdb

VOL_MAP="-v /var/smartem/data/influxdb:/var/lib/influxdb -v ${GIT}/services/influxdb/config/influxdb.conf:/etc/influxdb/influxdb.conf:ro"

PORT_MAP="-p 8083:8083 -p 8086:8086"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

# Finally run
sudo docker run --name ${NAME} ${PORT_MAP} ${VOL_MAP} -d -t ${IMAGE} -config /etc/influxdb/influxdb.conf

# generate conf: docker run --rm influxdb influxd config > influxdb.conf
# create db: curl -G http://localhost:8086/query --data-urlencode "q=CREATE DATABASE mydb"