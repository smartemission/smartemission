#!/bin/bash
#
# ETL for creating calibration model from Smart Emission Extracted DB data and
# RIVM 'ground truth' data.
#

STETL_ARGS="stetl -c calibrator.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
INFLUX_HOST=influxdb
PG_HOST=postgis
IMAGE=smartemission/stetl:latest
NAME="stetl_calibrate"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --network="se_back" -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
