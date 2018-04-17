#!/bin/bash
#
# Run the Mosquitto MQTT Server server with mapping to local config
# Docker image: https://github.com/smartemission/docker-se-mosquitto based on
# https://hub.docker.com/r/toke/mosquitto/
#

docker-compose rm --force --stop
docker-compose up -d

# sudo docker logs --follow mosquitto
