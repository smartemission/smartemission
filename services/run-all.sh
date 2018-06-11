#!/bin/bash
#
# Start/run all Docker-based services.
#
script_dir=${0%/*}

SERVICES="traefik postgis phppgadmin influxdb influxdb-dc1 chronograf grafana geoserver sosemu mosquitto gost gostdashboard sos52n monitoring"
for SERVICE in ${SERVICES}
do
  echo "starting ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./run.sh
  popd
done
