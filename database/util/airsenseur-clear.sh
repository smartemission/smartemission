#!/bin/bash
#
# Delete the AirSensEUR related data. USE WITH CARE! IT DELETES ALL HISTORY OF STA PUBLICATION!
#
# Specific to the ASE project for EU JRC, 2018/2019.
#
SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}/../
. common.sh

# 0 Stop all ETL processes
# 1 delete ASE data harvested from smartem_raw.timeseries
# select count(gid) from smartem_raw.timeseries where device_id/10000 = 1182;
# DELETE FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;
# 2 reset harvester position to start of RIVM deployment (aug 1, 2018)
# UPDATE smartem_raw.harvester_progress SET day = 180801, hour = 1 WHERE device_id/10000 = 1182;

# 3 delete refined ASE data in smartem_refined.timeseries
# DELETE FROM smartem_refined.timeseries WHERE device_id/10000 = 1182;

psql -h ${PGHOST} ${PGDB} -f util/airsenseur-clear.sql
popd

# 4 delete refined data from SensorThings API
# https://data.smartemission.nl/gost/v1.0/Things?$filter=name%20eq%20%2711820001%27
# All: https://data.smartemission.nl/gost/v1.0/Things?$filter=properties/project_id%20eq%20%271182%27
python airsenseur_staclear.py https://test.smartemission.nl/gost/v1.0/ ${sta_user_extern} ${sta_password_extern}

# 5. restart InfluxDB harvesting then others
# Shorthand func to call InfluxDB REST Query API

# Delete refined data from InfluxDB
function query() {
    DB=$1
    QUERY="$2"
    echo "db=$DB - query: ${QUERY}"
    # See https://docs.influxdata.com/influxdb/v1.4/guides/querying_data/
    curl -G 'https://test.smartemission.nl/influxdb/query?pretty=true' \
	 -u ${influx_admin_user}:${influx_admin_password} \
	 --data-urlencode "db=${DB}" --data-urlencode \
	 "q=${QUERY}"
}

query smartemission "DELETE from joserefined where station = '11820001'"
query smartemission "DELETE from joserefined where station = '11820002'"
query smartemission "DELETE from joserefined where station = '11820003'"
query smartemission "DELETE from joserefined where station = '11820004'"
query smartemission "DELETE from joserefined where station = '11820005'"
query smartemission "SELECT * from joserefined where station = '11820001' limit 2"
query smartemission "SELECT * from joserefined where station = '11820002' limit 2"
query smartemission "SELECT * from joserefined where station = '11820003' limit 2"
query smartemission "SELECT * from joserefined where station = '11820004' limit 2"
query smartemission "SELECT * from joserefined where station = '11820005' limit 2"
