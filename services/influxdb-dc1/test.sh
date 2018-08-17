#!/bin/bash
#
# Test DB for general health.
#       http://137.117.141.243:8086/query?

. influxdb.env

# Shorthand func to call InfluxDB REST Query API
function query() {
  DB=$1
  QUERY="$2"
  echo "db=$DB - query: ${QUERY}"
  # See https://docs.influxdata.com/influxdb/v1.4/guides/querying_data/
  curl -G 'http://dc1.smartemission.nl:8086/query?pretty=true' \
  -u ${INFLUXDB_READ_USER}:${INFLUXDB_READ_USER_PASSWORD} \
     --data-urlencode "db=${DB}" --data-urlencode \
     "q=${QUERY}"
}

#query _internal "SHOW GRANTS FOR ${influx_as_database}"
#query _internal "SHOW GRANTS FOR ${INFLUXDB_WRITE_USER}"
#
#query _internal "SHOW DATABASES"
#query _internal "SHOW USERS"

query ${INFLUXDB_DB} "SELECT * from ASE_NL_01 limit 2"
query ${INFLUXDB_DB} "SELECT * from ASE_NL_02 limit 2"
query ${INFLUXDB_DB} "SELECT * from ASE_NL_03 limit 2"
query ${INFLUXDB_DB} "SELECT * from ASE_NL_04 limit 2"
query ${INFLUXDB_DB} "SELECT * from ASE_NL_05 limit 2"

# Get the last N records
query ${INFLUXDB_DB} "SELECT * from ASE_NL_04 WHERE time > now() - 1h ORDER BY time DESC LIMIT 21"

# examples
# http://test.smartemission.nl:8086/query?db=smartemission&q=SELECT%20*%20from%20rivm%20limit%202
# http://local.smartemission.nl/influxdb/query?db=smartemission&q=SELECT%20*%20from%20rivm%20limit%202
