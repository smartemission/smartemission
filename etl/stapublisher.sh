#!/bin/bash
#
# ETL for publishing Smart Emission Refined DB data to a remote Sensor Things API (STA).
#

STETL_ARGS="stetl -c stapublisher.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
PG_HOST="postgis"
STA_HOST="gost"
LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${STA_HOST}:${STA_HOST}"
VOL_MAP="-v ${WORK_DIR}:${WORK_DIR}"

IMAGE=smartemission/stetl:latest
NAME="stetl_stapublish"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} ${LINK_MAP} ${VOL_MAP} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
