#!/bin/bash
#
# Init, database schema for raw harvested values. USE WITH CARE! IT DELETES ALL HISTORY!
#

. common.sh

SQL=schema/db-schema-gost-v0.6.sql
psql -h ${PGHOST} ${PGDB} -f ${SQL}
