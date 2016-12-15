#!/bin/bash
#
# ETL for extracting raw timeseries values from Smart Emission Raw DB data.
#

STETL_ARGS="-c extractor.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
PG_HOST=postgis
INFLUX_HOST=influxdb
IMAGE=geonovum/stetl:latest
NAME="stetl_extract"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} ${PORT_MAP} --link ${PG_HOST}:${PG_HOST} --link ${INFLUX_HOST}:${INFLUX_HOST} -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
