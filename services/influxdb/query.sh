#!/bin/bash
#
# Fire query on influxdb local instance.
#

pushd ../../etl/db
  . common.sh
popd

# Shorthand func to call InfluxDB REST Query API
function query() {
  QUERY="${@}"
  echo "query: ${QUERY}"

  # replace all blanks http://stackoverflow.com/questions/5928156/replace-a-space-with-a-period-in-bash
  # Basically urlencoding.
  QUERY=${QUERY// /%20}

  # Invoke curl to local InfluxDB instance to execute the query/command
  curl \
   -u ${influx_admin_user}:${influx_admin_password} \
   -H "Content-Type:text/plain" \
   -XPOST http://localhost:8086/query?q=${QUERY}
}

query ${@}
