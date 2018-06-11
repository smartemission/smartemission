#!/bin/bash
# See https://www.influxdata.com/blog/backuprestore-of-influxdb-fromto-docker-containers/

source influxdb.env

BACKUP_DIR="${SE_BACKUP_DIR}/${SE_CONTAINER_NAME}"
mkdir -p ${BACKUP_DIR}
rm -rf ${BACKUP_DIR}/*
TARGET_DUMP_FILE=${SE_BACKUP_DIR}/influxdb_${INFLUXDB_DB}_data.tar.gz

# On RUNNING container named influxdb
docker exec ${SE_CONTAINER_NAME} influxd backup -database ${INFLUXDB_DB} /backup

pushd ${SE_BACKUP_DIR}
	tar -cvzf ${TARGET_DUMP_FILE} ${SE_CONTAINER_NAME}
popd
