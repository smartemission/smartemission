#!/bin/bash
#
# Test DB for general health.
#

. influxdb.env

# Shorthand func to call InfluxDB REST Query API
function query() {
  DB=$1
  QUERY="$2"
  echo "db=$DB - query: ${QUERY}"
  # See https://docs.influxdata.com/influxdb/v1.4/guides/querying_data/
  curl -G 'http://localhost/influxdb/query?pretty=true' \
  -u ${INFLUXDB_ADMIN_USER}:${INFLUXDB_ADMIN_PASSWORD} \
     --data-urlencode "db=${DB}" --data-urlencode \
     "q=${QUERY}"
}

query _internal "SHOW GRANTS FOR ${INFLUXDB_READ_USER}"
query _internal "SHOW GRANTS FOR ${INFLUXDB_WRITE_USER}"

query _internal "SHOW DATABASES"
query _internal "SHOW USERS"

query ${INFLUXDB_DB} "SELECT * from rivm limit 2"

# examples
# http://test.smartemission.nl:8086/query?db=smartemission&q=SELECT%20*%20from%20rivm%20limit%202
# http://local.smartemission.nl/influxdb/query?db=smartemission&q=SELECT%20*%20from%20rivm%20limit%202
