#!/bin/bash
#
# Start/run all Docker-based services.
#
script_dir=${0%/*}

docker network create --driver=bridge se_front
docker network create --driver=bridge se_back

SERVICES="postgis influxdb chronograf grafana geoserver sos52n mosquitto gost gostdashboard monitoring web"
for SERVICE in ${SERVICES}
do
  echo "starting ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./run.sh
  popd
done
