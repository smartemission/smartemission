#!/bin/bash
#
# Init, database schema for metadata.
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f schema/db-schema-meta.sql
