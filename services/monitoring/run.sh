#!/bin/bash
#
source ../../etl/options/`hostname`.args

export se_host
export se_port
export GMAIL_ACCOUNT
export GMAIL_AUTH_TOKEN
export PARENT_HOST=`ip route show | grep docker0 | awk '{print \$9}'`

# Substitute env vars in .yaml
envsubst < alertmanager/config.yml > alertmanager/config-gen.yml
envsubst < prometheus/prometheus.yml > prometheus/prometheus-gen.yml

echo "External URL is http://${se_host}${se_port}"

UBUNTU_VERSION=`lsb_release -rs | cut -d'.' -f1`

case ${UBUNTU_VERSION} in
  14) echo "${UBUNTU_VERSION}"
    export CADVISOR_HOST=${PARENT_HOST}
	node_exporter/start.sh
	cadvisor/start.sh
	docker-compose -f docker-compose-14.04.yml -d up
  ;;
  16) echo "${UBUNTU_VERSION}"
    export CADVISOR_HOST=cadvisor
	docker-compose -d up
  ;;
  *) echo "${UBUNTU_VERSION} unsupported"; exit -1
  ;;
esac

