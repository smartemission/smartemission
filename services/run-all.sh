#!/bin/bash
#
# Start/run all services  (Docker Containers)
#
script_dir=${0%/*}

CONTAINERS="postgis geoserver sos52n web influxdb grafana"
for CONTAINER in ${CONTAINERS}
do
  echo "starting ${CONTAINER}"
  pushd ${script_dir}/${CONTAINER}
    ./run.sh
  popd
done
