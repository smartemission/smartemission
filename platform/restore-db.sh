#!/bin/bash
# restore van een complete DB
# Just van den Broecke 2016
#
# USAGE ./restore-db.sh <pad naar .bz2 dump bestand>

# Databases
export PGDB=gis
export PGUSER=docker
export PGPASSWORD=docker
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`

if [ $# -eq 0 ]
then
    echo "Geef .bz2 DB dump bestand bestand op als parameter."
    exit 1
fi

if [ ! -f $1 ]
then
    echo "Bestand $1 niet gevonden."
    exit 1
fi


bzip2 -c -d $1 | psql -h ${PGHOST} -U ${PGUSER} ${PGDB}
