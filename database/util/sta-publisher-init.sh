#!/bin/bash
#
# Init the SensorThings API Publisher. USE WITH CARE! IT DELETES ALL HISTORY OF STA PUBLICATION!
#

SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}/../
. common.sh
popd

psql -h ${PGHOST} ${PGDB} -c "UPDATE smartem_refined.etl_progress SET last_gid = -1, last_update = current_timestamp WHERE worker = 'stapublisher'"


