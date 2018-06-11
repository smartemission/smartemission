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

# Parameter ok
./stop.sh

source influxdb.env

DATA_DIR="${SE_DATA_DIR}/${SE_CONTAINER_NAME}"
BACKUP_DIR="${SE_BACKUP_DIR}/${SE_CONTAINER_NAME}"
IMAGE="influxdb:1.5.3"


# NB possibly best to make InfluxDB empty (db-init-influxdb.sh script)!
# otherwise this issue: https://github.com/influxdata/influxdb/issues/8320
# and restore just one DB...
rm -rf ${DATA_DIR}
mkdir -p ${DATA_DIR}

rm -rf ${BACKUP_DIR}
mkdir -p ${BACKUP_DIR}

pushd ${SE_BACKUP_DIR}
	tar xzvf ${DUMP_FILE}
popd


# On STOPPED container named influxdb
docker run --rm \
  --entrypoint /bin/bash \
  -v ${DATA_DIR}:/var/lib/influxdb \
  -v ${BACKUP_DIR}:/backup \
  ${IMAGE} \
  -c "influxd restore -metadir /var/lib/influxdb/meta -datadir /var/lib/influxdb/data -database ${INFLUXDB_DB} /backup"

# ./run.sh
