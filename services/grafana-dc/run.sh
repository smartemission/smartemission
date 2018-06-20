#!/bin/bash
#
# Run Grafana using smartemission/se-grafana-dc:5.1.3-1
#

export HOSTNAME

docker-compose rm --force --stop
docker-compose up -d

