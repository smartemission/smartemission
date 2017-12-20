#!/bin/bash
# See https://www.influxdata.com/blog/backuprestore-of-influxdb-fromto-docker-containers/

NAME="influxdb"
BACKUP_DIR="/var/smartem/backup/influxdb"

DBS="airsenseur smartemission"
for DB in ${DBS}
do
	# On RUNNING container named influxdb
	rm -rf ${BACKUP_DIR}/${DB}.backup
	docker exec ${NAME} influxd backup -database ${DB} /backup/${DB}.backup
done
