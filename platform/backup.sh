#!/bin/bash
#
# Routine backup for all data of the platform.
#
# Just van den Broecke - 2016
#

WEEK_DAY=`date +%w`
MONTH_DAY=`date +%d`
MONTH=`date +%m`

BACKUP_DIR=/var/smartem/backup
mkdir -p ${BACKUP_DIR}

# GeoServer data
GS_DIR=/var/smartem/data/geoserver
pushd ${GS_DIR}
  tar -cvzf ${BACKUP_DIR}/geoserver_data.tar.gz geoserver
popd

# Databases
export PGUSER=docker
export PGPASSWORD=docker
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`

LOG_FILE=${BACKUP_DIR}/db_backup.log

#
# Function : dump_db
# Purpose  : dump single PG DB
#
function dump_db() {
    DB=$1
    echo "START Dump ${DB} op `date`"
    pg_dump -h ${PGHOST} --clean ${DB} | bzip2 --best > ${BACKUP_DIR}/${DB}.sql.bz2
    echo "END Dump ${DB} op `date`"
}

echo "START backup databases on `date`" > ${LOG_FILE}

DBS="postgres gis"
for DB in ${DBS}
do
    dump_db ${DB} >> ${LOG_FILE} 2>&1
done

echo "END backup databases op `date`" >> ${LOG_FILE}


# Now sync to backup server
