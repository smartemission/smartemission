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
INFLUX_CMD="docker exec ${SE_CONTAINER_NAME} influx -host 127.0.0.1 -port 8086 -database ${INFLUXDB_DB} -username ${INFLUXDB_ADMIN_USER} -password ${INFLUXDB_ADMIN_PASSWORD} -execute "
# First must delete database otherwise meta restore errors
echo "DROP DATABASE ${INFLUXDB_DB}..."
${INFLUX_CMD} "DROP DATABASE ${INFLUXDB_DB}"

echo "Restore ${INFLUXDB_DB} from ${CONTAINER_BACKUP_DIR} ..."
docker exec ${SE_CONTAINER_NAME} influxd restore -portable -db ${INFLUXDB_DB} -newdb ${INFLUXDB_DB} /backup/${INFLUXDB_DB}

# Permissions are somehow not set, users should still exist
echo "Restore permissions for users ${INFLUXDB_READ_USER} and ${INFLUXDB_WRITE_USER} ..."
${INFLUX_CMD} "GRANT READ ON ${INFLUXDB_DB} TO ${INFLUXDB_READ_USER}"
${INFLUX_CMD} "GRANT ALL ON ${INFLUXDB_DB} TO ${INFLUXDB_WRITE_USER}"

# Cleanup
echo "Removing unpacked backup in ${BACKUP_DIR} ..."
rm -rf ${BACKUP_DIR}
