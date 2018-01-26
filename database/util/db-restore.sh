#!/bin/bash
# restore van een complete DB of schema dump
# Just van den Broecke 2017
#
# USAGE ./db-restore.sh <pad naar dump bestand>

# Set credentials
SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}/../
. common.sh
popd

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


function __msg() {
	printf -- "`date` - $1\n"
}


function __restore {
	# bzip2 -c -d $1 | psql -h ${PGHOST} -U ${PGUSER} ${PGDB}

	# Restore data (db or schema) from dump file
	__msg "Restoring $PGDUMPFILE in db $PGDB (duurt even...)"
	cmd="pg_restore -v -d $PGDB --no-owner --clean -Fc -U $PGUSER -h $PGHOST $PGDUMPFILE"
	__msg "execute: "$cmd""
	$cmd

	# Basic Check
	__msg "bestand $PGDUMPFILE ingelezen..."
}

__restore
