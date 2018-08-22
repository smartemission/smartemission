#!/bin/bash
# See https://www.influxdata.com/blog/backuprestore-of-influxdb-fromto-docker-containers/
# NB need to stop monitoring as influxdb will not stop because of cAdvisor lock!!!

if [ $# -eq 0 ]
then
    echo "Geef DB InfluxDB dump bestand bestand op als parameter."
    exit 1
fi

DUMP_FILE=$1

if [ ! -f ${DUMP_FILE} ]
then
    echo "Bestand ${DUMP_FILE} niet gevonden."
    exit 1
fi


SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}
	if [ ! -f influxdb.env ]
	then
	    echo "Bestand influxdb.env niet gevonden."
	    exit 1
	fi
    source influxdb.env

	# Parameter ok
	./stop.sh
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

if [ -z "${INFLUXDB_DB}" ]
then
    echo "INFLUXDB_DB not set"
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

pushd ${SE_BACKUP_DIR}/${SE_CONTAINER_NAME}
	tar xzvf ${DUMP_FILE}
popd


# On RUNNING container named influxdb
docker exec ${SE_CONTAINER_NAME} influxd restore -portable -db ${INFLUXDB_DB} -newdb ${INFLUXDB_DB} /backup/${INFLUXDB_DB}
