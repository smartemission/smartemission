#!/bin/bash
#
# Run the app
#

docker-compose rm --force --stop
docker-compose up -d
