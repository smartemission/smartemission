#!/bin/bash
#
# Generic ETL entry: override with specific ETL config and args file.
#

WORK_DIR=/work

cd ${WORK_DIR}

# Shorthand
function log() {
	echo "entry.sh: $1"
}

# Shorthand
function error() {
	log "$@"
	exit -1
}

# ETL Process can be specified via env var or argument
if [ "${ETL_PROCESS}x" = "x" ];
then
	ETL_PROCESS="$1"
fi

# ETL Process can be specified via env var or argument
if [ "${ETL_PROCESS}x" = "x" ];
then
	error "Error: no ETL process specified"
fi

ETL_CONFIG_FILE=config/${ETL_PROCESS}.cfg
if [ ! -f ${ETL_CONFIG_FILE} ]
then
	error "Error: cannot find ETL config file: ${ETL_CONFIG_FILE}"
else
	log "OK using config file: ${ETL_CONFIG_FILE}..."
fi

# Start Stetl with config file
export PYTHONPATH=${WORK_DIR}:${PYTHONPATH}
stetl -c ${ETL_CONFIG_FILE} -a options/default.args
