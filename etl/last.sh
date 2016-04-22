#!/bin/bash
#
# ETL for reading last values from Smart Emission CityGIS Raw Sensor API
#

STETL_ARGS="-c last.cfg -a options/docker.args"
WORK_DIR="`pwd`"
PG_HOST=postgis

sudo docker run --link ${PG_HOST}:${PG_HOST} -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} -t -i geonovum/stetl ${STETL_ARGS}
