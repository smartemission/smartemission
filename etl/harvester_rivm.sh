#!/bin/bash
#
# ETL for reading last values from from the RIVM LML SOS Rest API
#

STETL_ARGS="stetl -c harvester_rivm.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
IMAGE=smartemission/stetl:latest
NAME="stetl_harvest_rivm"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --network="se_back" -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
