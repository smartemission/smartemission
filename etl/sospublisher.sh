#!/bin/bash
#
# ETL for publishing Smart Emission Refined DB data to a SOS.
#

STETL_ARGS="-c sospublisher.cfg -a options/`hostname`.args"
WORK_DIR="`pwd`"
PG_HOST="postgis"
SOS52N_HOST="sos52n"
LINK_MAP="--link ${PG_HOST}:${PG_HOST} --link ${SOS52N_HOST}:${SOS52N_HOST}"
VOL_MAP="-v ${WORK_DIR}:${WORK_DIR}"

IMAGE=geonovum/stetl:latest
NAME="stetl_sospublish"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} ${LINK_MAP} ${VOL_MAP} -w ${WORK_DIR} ${IMAGE} ${STETL_ARGS}
