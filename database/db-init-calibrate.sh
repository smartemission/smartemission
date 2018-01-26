#!/bin/bash
#
# Init, database schema for calibration models. USE WITH CARE! IT DELETES ALL
# HISTORY!
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f schema/db-schema-calibrate.sql
