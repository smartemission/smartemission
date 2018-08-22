#!/bin/bash
#
# Routine backup for all data of the platform.
#
# Just van den Broecke - 2018
#

BACKUP_DIR=/var/smartem/backup

echo "START restore PG databases on `date`"

SCHEMAS="smartem_rt smartem_raw smartem_refined smartem_extracted smartem_harvest_rivm smartem_calibrated sos52n1 v1"
for SCHEMA in ${SCHEMAS}
do
	BACKUP_FILE=${BACKUP_DIR}/gis-${SCHEMA}.dmp
	./restore-db.sh ${BACKUP_FILE}
done

echo "END restore PG databases op `date`"

#BACKUP_FILE="${BACKUP_DIR}/influxdb_smartemission_data.tar.gz"
#pushd ../services/influxdb
#  ./restore.sh ${BACKUP_FILE}
#popd

