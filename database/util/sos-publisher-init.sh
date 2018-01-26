#!/bin/bash
#
# Init the SOS Publisher. USE WITH CARE! IT DELETES ALL HISTORY OF SOS PUBLICATION!
#

pushd ..
. common.sh
popd


psql -h ${PGHOST} ${PGDB} -c "UPDATE smartem_refined.etl_progress SET last_gid = -1, last_update = current_timestamp WHERE worker = 'sospublisher'"

