#!/bin/bash
#
# ETL for reading last values from Smart Emission CityGIS Raw Sensor API
#
export PGUSER=docker
export PGPASSWORD=docker
# Use local connection, we do not expose PG to outside world
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`
export PGDB=gis
