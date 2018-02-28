#!/bin/bash
#
/bin/rm -f alertmanager/config-gen.yml  prometheus/prometheus-gen.yml

UBUNTU_VERSION=`lsb_release -rs | cut -d'.' -f1`

case ${UBUNTU_VERSION} in
  14) echo "${UBUNTU_VERSION}"
	docker-compose -f docker-compose-14.04.yml stop
	docker-compose -f docker-compose-14.04.yml rm -f
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

