#!/bin/bash
#
# Init, database schema for metadata.
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f db-schema-meta.sql
