#!/bin/bash
#
# Routine backup for all data of the platform.
#
# Just van den Broecke - 2016
#

DATE=`date +%Y-%m-%d`
YEAR=`date +%Y`
WEEK_DAY=`date +%w`
MONTH_DAY=`date +%d`
MONTH=`date +%m`

BACKUP_DIR=/var/smartem/backup
mkdir -p ${BACKUP_DIR}

# GeoServer data and SOS52N config data
SE_DATA_DIR=/var/smartem/data
pushd ${SE_DATA_DIR}
  tar -cvzf ${BACKUP_DIR}/geoserver_data.tar.gz geoserver
  tar -cvzf ${BACKUP_DIR}/sos52n_data.tar.gz sos52n
popd

# Databases
export PGUSER=docker
export PGPASSWORD=docker
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`

LOG_FILE=${BACKUP_DIR}/backup_db.log

#
# Function : dump_db
# Purpose  : dump single PG DB
#
function dump_db_old() {
    DB=$1
    SCHEMA="all"
	if [ $# -eq 2 ]
	then
        SCHEMA=$2
        SCHEMA_ARG="--schema=${SCHEMA}"
	fi

    echo "START Dump ${DB} schema ${SCHEMA} op `date`"
    pg_dump -h ${PGHOST} --clean ${SCHEMA_ARG} ${DB} | bzip2 --best > ${BACKUP_DIR}/${DB}-${SCHEMA}.sql.bz2
    echo "END Dump ${DB} schema ${SCHEMA} op `date`"
}

#
# Functie : dump_db
# Doel    : dump database alles of enkel schema
#
function dump_db() {
	DB=$1
    SCHEMA="all"
	if [ $# -eq 2 ]
	then
        SCHEMA=$2
        SCHEMA_ARG="--schema=${SCHEMA}"
	fi

    echo "START Dump ${DB} schema ${SCHEMA} op `date`"
	# pg_dump --clean ${ARGS} ${DB} | bzip2 --best > ${BACKUP_DIR}/${DB}.sql.bz2
	pg_dump \
	${SCHEMA_ARG} \
	-h ${PGHOST} \
	--format custom \
	--no-password \
	--no-owner \
	--compress 7 \
	--encoding UTF8 \
	--verbose \
	--file ${BACKUP_DIR}/${DB}-${SCHEMA}.dmp \
	${DB}

    echo "END Dump ${DB} schema ${SCHEMA} op `date`"
}

echo "START backup databases on `date`" > ${LOG_FILE}

dump_db postgres >> ${LOG_FILE} 2>&1

SCHEMAS="smartem_rt smartem_raw smartem_refined sos52n1"
for SCHEMA in ${SCHEMAS}
do
	dump_db gis ${SCHEMA} >> ${LOG_FILE} 2>&1
done

echo "END backup databases op `date`" >> ${LOG_FILE}

# Now sync to backup server
RSYNC="rsync -e ssh -alzvx --delete "
BACKUP_HOST="vps68271@backup"

# We will have last 7 days always
${RSYNC} ${BACKUP_DIR}/ ${BACKUP_HOST}:`hostname`-weekday-${WEEK_DAY}/  >> ${LOG_FILE}

# At the start of each month we save the backup of the last day of previous month
${RSYNC} ${BACKUP_DIR}/ ${BACKUP_HOST}:`hostname`-${YEAR}-${MONTH}/  >> ${LOG_FILE}

# To inspect from admin
cp ${LOG_FILE} /var/smartem/log
