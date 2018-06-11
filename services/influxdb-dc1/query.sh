#!/bin/bash
#
# Fire query on influxdb local instance.
# usage: ./query.sh host db 'my query'
# examples:
# ./query.sh test.smartemission.nl airsenseur "SELECT sampleRawVal FROM JustObjects1"
# ./query.sh test.smartemission.nl airsenseur "SELECT sampleRawVal FROM JustObjects1 WHERE \"name\" = 'NO2-B43F'"
# ./query.sh test.smartemission.nl airsenseur "SHOW SERIES FROM Geonovum1"
# ./query.sh test.smartemission.nl airsenseur 'DROP MEASUREMENT JustObjects1'

source influxdb.env

INFLUX_HOST=$1
INFLUX_DB=$2

# Shorthand func to call InfluxDB REST Query API
function query() {
  QUERY="${1}"
  echo "host: ${INFLUX_HOST} db=${INFLUX_DB} query: ${QUERY}"

  # replace all blanks http://stackoverflow.com/questions/5928156/replace-a-space-with-a-period-in-bash
  # Basically urlencoding.
  # QUERY=${QUERY// /%20}

  # Invoke curl to local InfluxDB instance to execute the query/command   OLD
#  curl \
#   -u ${influx_admin_user}:${influx_admin_password} \
#   -H "Content-Type:text/plain" \
#   -XPOST http://${INFLUX_HOST}:8086/query?q=${QUERY}


	# example curl
	# curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=mydb" --data-urlencode "q=SELECT value FROM cpu_load_short WHERE region='us-west';SELECT count(value) FROM cpu_load_short WHERE region='us-west'"

   curl  -u ${influx_admin_user}:${influx_admin_password} \
     -GET "http://${INFLUX_HOST}:8086/query?pretty=true" \
     --data-urlencode "db=${INFLUX_DB}" \
     --data-urlencode "q=${QUERY}"
}

#

query "$3"
