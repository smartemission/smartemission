#!/bin/bash
#
# Init, database schema for last values.
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f db-schema-last.sql
