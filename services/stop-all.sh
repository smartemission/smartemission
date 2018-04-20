#!/bin/bash
#
# Stop all Docker-based services.
#
script_dir=${0%/*}

SERVICES="monitoring gostdashboard geoserver sosemu gost mosquitto phppgadmin postgis grafana chronograf influxdb traefik"
for SERVICE in ${SERVICES}
do
  echo "stopping ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./stop.sh
  popd
done
