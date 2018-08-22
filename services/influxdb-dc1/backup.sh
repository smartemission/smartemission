#!/bin/bash
# See https://www.influxdata.com/blog/backuprestore-of-influxdb-fromto-docker-containers/

SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}
	if [ ! -f influxdb.env ]
	then
	    echo "Bestand influxdb.env niet gevonden."
	    exit 1
	fi
    source influxdb.env
popd

# Make sure vars are set
if [ -z "${SE_BACKUP_DIR}" ]
then
    echo "SE_BACKUP_DIR not set"
    exit 1
fi

if [ -z "${SE_CONTAINER_NAME}" ]
then
    echo "SE_CONTAINER_NAME not set"
    exit 1
fi

BACKUP_DIR="${SE_BACKUP_DIR}/${SE_CONTAINER_NAME}/${INFLUXDB_DB}"
if [ -z "${BACKUP_DIR}" ]
then
    echo "BACKUP_DIR not set"
    exit 1
fi

rm -rf ${BACKUP_DIR}
mkdir -p ${BACKUP_DIR}

TARGET_DUMP_FILE=${SE_BACKUP_DIR}/${SE_CONTAINER_NAME}_${INFLUXDB_DB}_data.tar.gz

# On RUNNING container named influxdb
docker exec ${SE_CONTAINER_NAME} influxd backup -portable -database ${INFLUXDB_DB} /backup/${INFLUXDB_DB}

pushd ${SE_BACKUP_DIR}/${SE_CONTAINER_NAME}
	tar -cvzf ${TARGET_DUMP_FILE} ${INFLUXDB_DB}
popd
