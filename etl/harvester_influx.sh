#!/bin/bash
#
# ETL for reading last values from Smart Emission CityGIS Raw Sensor API
#

STETL_ARGS="stetl -c harvester_influx.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
PG_HOST=postgis
INFLUX_HOST=influxdb
IMAGE=smartemission/stetl:latest
NAME="stetl_harvest_influx"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --link ${PG_HOST}:${PG_HOST} --link ${INFLUX_HOST}:${INFLUX_HOST} -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
