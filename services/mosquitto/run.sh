#!/bin/bash
#
# Run the Mosquitto MQTT Server server with mapping to local config
# Docker image: https://hub.docker.com/r/toke/mosquitto/
# GitHub: https://github.com/toke/docker-mosquitto
#

GIT="/opt/geonovum/smartem/git"
CONFIG_DIR="${GIT}/services/mosquitto/config"
DATA_DIR="/var/smartem/data/mosquitto"
LOG_DIR="/var/smartem/log/mosquitto"

# Optional dir create
sudo mkdir -p ${DATA_DIR}
sudo mkdir -p ${LOG_DIR}
sudo chmod 777 ${LOG_DIR}

NAME="mosquitto"
IMAGE="toke/mosquitto:latest"

# Define Volume mappings, map local config file
# See https://github.com/toke/docker-mosquitto/blob/master/README.md
VOL_MAP="-v ${DATA_DIR}:/mqtt/data -v ${CONFIG_DIR}/mosquitto.conf:/mqtt/config/mosquitto.conf:ro -v ${LOG_DIR}:/mqtt/log"

# If we need to expose host
PORT_MAP="-p 1883:1883 -p 9001:9001"


# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1
sudo docker run --name ${NAME} --network="se_back" ${PORT_MAP} ${VOL_MAP} -d ${IMAGE}

# sudo docker logs --follow mosquitto
