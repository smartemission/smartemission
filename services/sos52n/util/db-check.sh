#!/bin/bash

DB_USER=docker
DB_PASSWORD=docker
DB_NAME=gis
SOS_DB_SCHEMA=sos52n1
SOS_DB_TABLE=observation

export PGUSER=${DB_USER}
export PGPASSWORD=${DB_PASSWORD}
export DB_HOST=`sudo docker inspect --format '{{ .NetworkSettings.Networks.se_back.IPAddress }}' postgis`


# Check if we need to create DB tables
# See https://www.postgresql.org/docs/current/static/functions-info.html#FUNCTIONS-INFO-CATALOG-TABLE

echo "Check if DB populated DB_NAME='${DB_NAME}'"

# First check if  DB Schema present: if not no use to proceed.
echo "Check if ${SOS_DB_SCHEMA} exists"
schema_present=$(psql -qtAX -h "${DB_HOST}" -c "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '${SOS_DB_SCHEMA}')" ${DB_NAME})
# echo "schema_present = ${schema_present}"
if [ "${schema_present}" != "t" ]
then
	echo "Schema ${SOS_DB_SCHEMA} does not exist, create this first, quitting..."
	exit -1
else
	echo "OK: Schema ${SOS_DB_SCHEMA} exists"
fi

echo "Check if ${SOS_DB_SCHEMA}.${SOS_DB_TABLE} exists"
table_present=$(psql -qtAX -h "${DB_HOST}" -c "select count(to_regclass('${SOS_DB_SCHEMA}.${SOS_DB_TABLE}'))" ${DB_NAME})
# echo "table_present=${table_present}"
if [ "${table_present}" = "0" ]
then
	echo "Creating Postgres DB tables..."
	psql -q -h "${DB_HOST}" "${DB_NAME}" -f db-init.sql
else
	echo "OK: Postgres DB already populated"
fi
