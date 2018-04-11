#!/bin/bash
#
# Start/run all Docker-based services.
#
script_dir=${0%/*}

#docker network create --driver=bridge se_front
#docker network create --driver=bridge se_back

SERVICES="admin heron home smartapp waalkade"
for SERVICE in ${SERVICES}
do
  echo "starting ${SERVICE}"
  pushd ${script_dir}/${SERVICE}
    ./run.sh
  popd
done
