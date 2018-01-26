#!/bin/bash
#
# Dump raw harvested values as JSON file.
#

SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}/../
. common.sh
popd

psql -h ${PGHOST} ${PGDB} -f db-dump-raw.sql
