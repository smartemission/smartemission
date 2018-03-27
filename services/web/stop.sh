#!/bin/bash
#
# docker stop web
# Stop and remove possibly old containers
docker-compose stop
docker-compose rm -f
