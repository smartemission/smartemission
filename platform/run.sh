#!/bin/bash
#
# This runs all assets (mainly Docker images) for SmartEmission Data Platform
# You must first have done ./build.sh
#
# Just van den Broecke - 2016
#

pushd ../services
./run-all.sh
popd
crontab cronfile.txt
