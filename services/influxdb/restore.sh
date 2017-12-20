#!/bin/bash
# See https://www.influxdata.com/blog/backuprestore-of-influxdb-fromto-docker-containers/
# NB need to stop monitoring as influxdb will not stop because of cAdvisor lock!!!

DATA_DIR="/var/smartem/data/influxdb"
BACKUP_DIR="/var/smartem/backup/influxdb"
NAME="influxdb"
IMAGE="influxdb:1.1.1"

DBS="airsenseur smartemission"

./stop.sh
for DB in ${DBS}
do
	# On STOPPED container named influxdb
	docker run --rm \
	  --entrypoint /bin/bash \
	  -v ${DATA_DIR}:/var/lib/influxdb \
	  -v ${BACKUP_DIR}:/backup \
	  ${IMAGE} \
	  -c "influxd restore -metadir /var/lib/influxdb/meta -datadir /var/lib/influxdb/data -database ${DB} /backup"
done

# ./run.sh