#!/bin/bash
#
# ETL for publishing Smart Emission Refined DB data to a SOS.
#

STETL_ARGS="stetl -c sospublisher.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
VOL_MAP="-v ${WORK_DIR}:${WORK_DIR}"
IMAGE=smartemission/stetl:latest
NAME="stetl_sospublish"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --network="se_back" ${VOL_MAP} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
