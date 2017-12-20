#!/bin/bash
# See https://www.influxdata.com/blog/backuprestore-of-influxdb-fromto-docker-containers/

NAME="influxdb"
BACKUP_DIR="/var/smartem/backup/influxdb"

DBS="airsenseur smartemission"
rm -rf ${BACKUP_DIR}/*
for DB in ${DBS}
do
	# On RUNNING container named influxdb
	docker exec ${NAME} influxd backup -database ${DB} /backup
done
