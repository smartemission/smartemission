#!/bin/bash
#
# Start/run all Docker-based services.
#
script_dir=${0%/*}

SERVICES="postgis influxdb grafana geoserver sos52n mosquitto gost monitoring web"
for SERVICE in ${SERVICES}
do
  echo "starting ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./run.sh
  popd
done
