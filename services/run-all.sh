#!/bin/bash
#
# Start/run all Docker-based services.
#
script_dir=${0%/*}

docker network create --driver=bridge se_front
docker network create --driver=bridge se_back

SERVICES="traefik postgis influxdb chronograf grafana geoserver sos52n sosemu mosquitto gost gostdashboard monitoring"
for SERVICE in ${SERVICES}
do
  echo "starting ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./run.sh
  popd
done
