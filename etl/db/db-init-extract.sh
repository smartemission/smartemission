#!/bin/bash
#
# Init, database schema for extracted values. USE WITH CARE! IT DELETES ALL
# HISTORY!
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f db-schema-extract.sql
