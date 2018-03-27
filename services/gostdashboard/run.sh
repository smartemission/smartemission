#!/bin/bash
#
# Run the SensorThings API (STA) GOST server Dashboard UI
# Docker image: https://store.docker.com/community/images/geodan/gost-dashboard
#

docker-compose rm --force --stop
docker-compose up -d
# docker logs --follow gostdashboard
