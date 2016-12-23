#!/bin/bash
#
# Init, database schema for influxdb. USE WITH CARE! IT DELETES ALL DATA!
#

. common.sh

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

# Initialize the DB
query "CREATE USER ${influx_admin_user} WITH PASSWORD '${influx_admin_password}' WITH ALL PRIVILEGES"
query "SHOW GRANTS FOR ${influx_admin_user}"

# Initialize for Smart Emission
query "DROP DATABASE ${influx_se_database}"
query "CREATE DATABASE ${influx_se_database}"
query "DROP USER ${influx_se_writer}"
query "DROP USER ${influx_se_reader}"
query "CREATE USER ${influx_se_writer} WITH PASSWORD '${influx_se_writer_password}'"
query "CREATE USER ${influx_se_reader} WITH PASSWORD '${influx_se_reader_password}'"
query "GRANT ALL ON ${influx_se_database} TO ${influx_se_writer}"
query "GRANT READ ON ${influx_se_database} TO ${influx_se_reader}"
query "SHOW GRANTS FOR ${influx_se_writer}"
query "SHOW GRANTS FOR ${influx_se_reader}"

# Initialize for AirSensEUR
query "DROP DATABASE ${influx_as_database}"
query "CREATE DATABASE ${influx_as_database}"
query "DROP USER ${influx_as_writer}"
query "DROP USER ${influx_as_reader}"
query "CREATE USER ${influx_as_writer} WITH PASSWORD '${influx_as_writer_password}'"
query "CREATE USER ${influx_as_reader} WITH PASSWORD '${influx_as_reader_password}'"
query "GRANT ALL ON ${influx_as_database} TO ${influx_as_writer}"
query "GRANT READ ON ${influx_as_database} TO ${influx_as_reader}"
query "SHOW GRANTS FOR ${influx_as_writer}"
query "SHOW GRANTS FOR ${influx_as_reader}"

query "SHOW DATABASES"
query "SHOW USERS"
