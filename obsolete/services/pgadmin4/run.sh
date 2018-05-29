#!/bin/bash
#
# Run the SensorThings API (STA) GOST server with mapping to local config
# Docker image: https://hub.docker.com/r/geodan/gost/
#

# Need HOSTNAME within docker-compose for host-specific path to env file.
export HOSTNAME

docker-compose rm --force --stop
docker-compose up -d
