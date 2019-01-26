#!/bin/bash

export HOSTNAME
export HTTP_PORT=80

if [ ${HOSTNAME} = "nusa" ]
then
	HTTP_PORT=8001
fi

# Stop and remove possibly old containers
docker-compose stop
docker-compose rm -f

chmod 600 config/acme.json

# Finally run
docker-compose up -d
