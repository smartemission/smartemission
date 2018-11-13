#!/bin/bash
#
# Generic run process to call SE Stetl Docker container.
#

# Shorthand
function log() {
	echo "run.sh: $@"
}

# ETL Process must be as first argument
ETL_PROCESS="$1"
if [ "${ETL_PROCESS}x" = "x" ];
then
	log "Error: no ETL process specified, usage ./run.sh <etl process> e.g. ./run.sh last"
	exit -1
fi

IMAGE=smartemission/se-stetl:1.0.26
NAME="stetl_${ETL_PROCESS}"
NETWORK="--network=se_back"
ETL_DEFAULT_ARGS="/work/options/default.args"
ETL_ARGS="${PWD}/options/`hostname`.args"

# Stop and remove possibly old containers
docker stop ${NAME} > /dev/null 2>&1
docker rm ${NAME} > /dev/null 2>&1

# Run Docker container: map host-specific args over default args
docker run -t --name ${NAME} ${NETWORK} -v ${ETL_ARGS}:${ETL_DEFAULT_ARGS} ${IMAGE} ${ETL_PROCESS}
