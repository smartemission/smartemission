#!/bin/bash
#
# Stop all Docker-based services.
#
script_dir=${0%/*}

SERVICES="web monitoring gostdashboard geoserver sos52n gost mosquitto postgis grafana influxdb "
for SERVICE in ${SERVICES}
do
  echo "stopping ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./stop.sh
  popd
done
