#!/bin/bash
#
# Fire query on influxdb local instance.
# usage: ./query.sh host db 'my query'
# examples:
# ./query.sh dc1.smartemission.nl airsenseur "SELECT sampleRawVal FROM ASE_NL_01"
# ./query.sh dc1.smartemission.nl airsenseur "SELECT sampleRawVal FROM ASE_NL_01 WHERE \"name\" = 'NO2B43F'"
# ./query.sh dc1.smartemission.nl airsenseur "SHOW SERIES FROM ASE_NL_02"
# ./query.sh dc1.smartemission.nl airsenseur 'DROP MEASUREMENT ASE_NL_01'

source influxdb.env

INFLUX_HOST=$1
INFLUX_DB=$2

# Shorthand func to call InfluxDB REST Query API
function query() {
  QUERY="${1}"
  echo "host: ${INFLUX_HOST} db=${INFLUX_DB} query: ${QUERY}"

	# example curl
	# curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=mydb" --data-urlencode "q=SELECT value FROM cpu_load_short WHERE region='us-west';SELECT count(value) FROM cpu_load_short WHERE region='us-west'"

   curl  -u ${INFLUXDB_ADMIN_USER}:${INFLUXDB_ADMIN_PASSWORD} \
     -GET "http://${INFLUX_HOST}:8086/query?pretty=true" \
     --data-urlencode "db=${INFLUX_DB}" \
     --data-urlencode "q=${QUERY}"
}

#

query "$3"
