#!/bin/bash
#
# This stops all assets (mainly Docker images) for SmartEmission Data Platform
# You must first have done ./start.sh
#
# Just van den Broecke - 2016
#

script_dir=${0%/*}

crontab -r

pushd ${script_dir}/../services
./stop-all.sh
popd

pushd ${script_dir}/../apps
./stop-all.sh
popd
