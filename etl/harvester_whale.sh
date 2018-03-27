#!/bin/bash
#
# ETL for reading last values from Smart Emission CityGIS/Intemo (Whale) Raw Sensor API
#

STETL_ARGS="stetl -c harvester_whale.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
IMAGE=smartemission/stetl:latest
NAME="whale_harvest"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --network="se_back" -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
