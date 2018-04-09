#!/bin/bash
#
# Run the Heron app
#

docker-compose rm --force --stop
docker-compose up -d
