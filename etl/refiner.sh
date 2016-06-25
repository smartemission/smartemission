#!/bin/bash
#
# ETL for refining raw timeseries values from Smart Emission Raw DB data.
#

STETL_ARGS="-c refiner.cfg -a options/docker.args"
WORK_DIR="`pwd`"
PG_HOST=postgis
IMAGE=geonovum/stetl:latest
NAME="stetl_refine"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --link ${PG_HOST}:${PG_HOST} -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
