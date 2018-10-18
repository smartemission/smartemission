#!/bin/bash

chmod 600 config/acme.json

# Stop and remove possibly old containers
docker-compose stop
docker-compose rm -f

# Finally run
docker-compose up -d
