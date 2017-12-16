#!/bin/bash
#
# Start/run all services  (Docker Containers)
#
script_dir=${0%/*}

CONTAINERS="postgis influxdb grafana geoserver sos52n mosquitto gost prometheus web"
for CONTAINER in ${CONTAINERS}
do
  echo "starting ${CONTAINER}"
  pushd ${script_dir}/${CONTAINER}
    ./run.sh
  popd
done
