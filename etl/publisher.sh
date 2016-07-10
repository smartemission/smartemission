#!/bin/bash
#
# ETL for refining raw timeseries values from Smart Emission Raw DB data.
#

STETL_ARGS="-c publisher.cfg -a options/docker.args"
WORK_DIR="`pwd`"
PG_HOST="postgis"
SOS52N_HOST="sos52n"
LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${SOS52N_HOST}:${SOS52N_HOST}"
VOL_MAP="-v ${WORK_DIR}:${WORK_DIR}"

IMAGE=geonovum/stetl:latest
NAME="stetl_publish"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} ${LINK_MAP} ${VOL_MAP} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
