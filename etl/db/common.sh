#!/bin/bash
#
# Variable settings shared by all scripts.
#

HNAME=`hostname`

echo "Using host-specific options for ${HNAME}"

pushd ../options
. ${HNAME}.args
popd

export PGUSER=${pg_user}
export PGPASSWORD=${pg_password}
export PGDB=${pg_database}

# Use local connection, we do not expose PG to outside world
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`
# export INFLUXHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' influxdb`
