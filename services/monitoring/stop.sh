#!/bin/bash
#
/bin/rm -f alertmanager/config-gen.yml  prometheus/prometheus-gen.yml

docker-compose stop
docker-compose rm -f
service node_exporter stop
