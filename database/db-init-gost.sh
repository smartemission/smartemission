#!/bin/bash
#
# Init, database schema for raw harvested values. USE WITH CARE! IT DELETES ALL HISTORY!
#

. common.sh

SQL=../services/gost/config/gost-init-db.sql
psql -h ${PGHOST} ${PGDB} -f ${SQL}
