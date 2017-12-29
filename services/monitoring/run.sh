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
node_exporter/start.sh
cadvisor/start.sh
docker-compose up -d
