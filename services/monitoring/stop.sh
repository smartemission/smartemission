#!/bin/bash
#
/bin/rm -f alertmanager/config-gen.yml  prometheus/prometheus-gen.yml

UBUNTU_VERSION=`lsb_release -rs | cut -d'.' -f1`

# Ubuntu 14.4 does not support Dockerized node-exporter and cAdvisor
# So use different docker-compose files, hacky but needed.
case ${UBUNTU_VERSION} in
  14) echo "${UBUNTU_VERSION}"
	docker-compose -f docker-compose-14.4.yml stop
	docker-compose -f docker-compose-14.4.yml rm -f
	node_exporter/stop.sh
	cadvisor/stop.sh
  ;;
  16) echo "${UBUNTU_VERSION}"
	docker-compose stop
	docker-compose rm -f
  ;;
  *) echo "${UBUNTU_VERSION} unsupported"; exit -1
  ;;
esac

