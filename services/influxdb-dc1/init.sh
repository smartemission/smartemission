#!/bin/bash
# See https://www.influxdata.com/blog/backuprestore-of-influxdb-fromto-docker-containers/
# NB need to stop monitoring as influxdb will not stop because of cAdvisor lock!!!

SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}
	if [ ! -f influxdb.env ]
	then
	    echo "Bestand influxdb.env niet gevonden."
	    exit 1
	fi
    source influxdb.env
popd

# On RUNNING container named influxdb
INFLUX_CMD="docker exec ${SE_CONTAINER_NAME} influx -host 127.0.0.1 -port 8086 -database ${INFLUXDB_DB} -username ${INFLUXDB_ADMIN_USER} -password ${INFLUXDB_ADMIN_PASSWORD} -execute "

echo "DROP DATABASE ${INFLUXDB_DB}..."
${INFLUX_CMD} "DROP DATABASE ${INFLUXDB_DB}"
