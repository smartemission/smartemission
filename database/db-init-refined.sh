#!/bin/bash
#
# Init, database schema for refined values. USE WITH CARE! IT DELETES ALL HISTORY!
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f schema/db-schema-refined.sql

echo "also may need to DROP SERIES FROM joserefined in InfluxDB"