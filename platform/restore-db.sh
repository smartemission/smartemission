#!/bin/bash
# restore van een complete DB
# Just van den Broecke 2016
#
# USAGE ./restore-db.sh <pad naar dump bestand>

# Databases
export PGDB=gis
export PGUSER=docker
export PGPASSWORD=docker
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`

if [ $# -eq 0 ]
then
    echo "Geef DB dump bestand bestand op als parameter."
    exit 1
fi

PGDUMPFILE=$1

if [ ! -f $PGDUMPFILE ]
then
    echo "Bestand $PGDUMPFILE niet gevonden."
    exit 1
fi


# bzip2 -c -d $1 | psql -h ${PGHOST} -U ${PGUSER} ${PGDB}

function __restore {

	# Restore data (db or schema) from dump file
	__msg "Restoring $PGDUMPFILE in db $PGDB (duurt even...)"
	cmd="pg_restore -v -d $PGDB --no-owner --clean -Fc -U $PGUSER -h $PGHOST $PGDUMPFILE"
	__msg "execute: "$cmd""
	$cmd

	# Basic Check
	__msg "bestand $PGDUMPFILE ingelezen..."
}

__restore
