#!/bin/bash
#
/bin/rm -f alertmanager/config-gen.yml  prometheus/prometheus-gen.yml

docker-compose stop
docker-compose rm -f
node_exporter/stop.sh
cadvisor/stop.sh
