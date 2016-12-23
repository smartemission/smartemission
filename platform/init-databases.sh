#!/bin/bash
#
# This initializes all databases.
# NB use only when setting up the platform!! It will clear all existing databases!!!
#
#
# Just van den Broecke - 2016
#

pushd ../services/postgis
  ./run.sh
popd

pushd ../services/influxdb
  ./run.sh
popd

pushd ../etl/db
  ./db-init-last.sh
  ./db-init-raw.sh
  ./db-init-refined.sh
  ./db-init-extract.sh
  ./db-init-influxdb.sh
  ./db-init-harvest-rivm.sh
popd

echo "READY: now run ./install.sh install SE Data Platform system daemon"
