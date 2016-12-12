#!/bin/bash
#
# Init the SensorThings API Publisher. USE WITH CARE! IT DELETES ALL HISTORY OF STA PUBLICATION!
#

script_dir=${0%/*}

pushd ${script_dir}
. common.sh

psql -h ${PGHOST} ${PGDB} -c "UPDATE smartem_refined.etl_progress SET last_gid = -1, last_update = current_timestamp WHERE worker = 'stapublisher'"

popd
