#!/bin/bash
#
# Stop all Docker-based services.
#
script_dir=${0%/*}

SERVICES="web monitoring gostdashboard geoserver sos52n sosemu gost mosquitto postgis grafana chronograf influxdb "
for SERVICE in ${SERVICES}
do
  echo "stopping ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./stop.sh
  popd
done

docker network rm se_back se_front
