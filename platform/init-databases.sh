#!/bin/bash
#
# This initializes all databases.
# NB use only when setting up the platform!! It will clear all existing databases!!!
#
#
# Just van den Broecke - 2016
#

docker network create --driver=bridge se_back

pushd ../services/postgis
  ./run.sh
popd

pushd ../database
  ./db-init-meta.sh
  ./db-init-last.sh
  ./db-init-raw.sh
  ./db-init-refined.sh
  ./db-init-extract.sh
  ./db-init-harvest-rivm.sh
  ./db-init-calibrate.sh
  ./db-init-gost.sh
popd

docker network rm se_back se_front

pushd ../services/postgis
  ./stop.sh
popd

echo "READY: now run ./install.sh install SE Data Platform system daemon"
