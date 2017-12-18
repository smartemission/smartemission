#!/bin/bash
#
source ../../etl/options/`hostname`.args

echo "External URL is http://${se_host}${se_port}"
docker-compose up -d
