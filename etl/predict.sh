#!/bin/bash
#
# ETL for applying calibration model on hourly Smart Emission refined measurements to predict hourly RIVM measurements.
#

STETL_ARGS="-c predict.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
INFLUX_HOST=influxdb
PG_HOST=postgis
IMAGE=geonovum/stetl:latest
NAME="stetl_predict"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --link ${PG_HOST}:${PG_HOST} --link ${INFLUX_HOST}:${INFLUX_HOST} -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
