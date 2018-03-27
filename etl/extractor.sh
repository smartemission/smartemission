#!/bin/bash
#
# ETL for extracting raw timeseries values from Smart Emission Raw DB data.
#

STETL_ARGS="stetl -c extractor.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
PG_HOST=postgis
INFLUX_HOST=influxdb
IMAGE=smartemission/stetl:latest
NAME="stetl_extract"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --network="se_back" -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
