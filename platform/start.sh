#!/bin/bash
#
# This runs all assets (mainly Docker images) for SmartEmission Data Platform
# You must first have done ./build.sh
#
# Just van den Broecke - 2016
#

script_dir=${0%/*}

docker network create --driver=bridge se_front
docker network create --driver=bridge se_back

pushd ${script_dir}/../services
./run-all.sh
popd

pushd ${script_dir}/../apps
./run-all.sh
popd

crontab ${script_dir}/cronfile.txt
