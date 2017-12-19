#!/bin/bash
#
source ../../etl/options/`hostname`.args

export se_host
export se_port
export GMAIL_ACCOUNT
export GMAIL_AUTH_TOKEN

# Substitute env vars in .yaml
envsubst < alertmanager/config.yml > alertmanager/config-gen.yml

echo "External URL is http://${se_host}${se_port}"
docker-compose up -d
