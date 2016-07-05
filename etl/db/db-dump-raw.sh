#!/bin/bash
#
# Dump raw harvested values as JSON file.
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f db-dump-raw.sql
