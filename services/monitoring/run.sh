#!/bin/bash
#
source ../../etl/options/`hostname`.args

export se_host
export se_port
export GMAIL_ACCOUNT
export GMAIL_AUTH_TOKEN
export PARENT_HOST=`ip route show | grep docker0 | awk '{print \$9}'`

echo "External URL is http://${se_host}${se_port}"

UBUNTU_VERSION=`lsb_release -rs | cut -d'.' -f1`
echo "Ubuntu version: ${UBUNTU_VERSION}"

case ${UBUNTU_VERSION} in
    14) export CADVISOR_HOST=${PARENT_HOST}
        export NODE_EXPORTER_HOST=${PARENT_HOST}
        export DOCKER_COMPOSE_YML="docker-compose-14.04.yml"
        node_exporter/start.sh
        cadvisor/start.sh
        ;;
    16) export CADVISOR_HOST=cadvisor
        export NODE_EXPORTER_HOST=${PARENT_HOST}
        export DOCKER_COMPOSE_YML="docker-compose.yml"
        ;;
    *) echo "${UBUNTU_VERSION} unsupported"; exit -1
       ;;
esac

# Substitute env vars in .yaml
envsubst < alertmanager/config.yml > alertmanager/config-gen.yml
envsubst < prometheus/prometheus.yml > prometheus/prometheus-gen.yml

docker-compose -f ${DOCKER_COMPOSE_YML} up -d
