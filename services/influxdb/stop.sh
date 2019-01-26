#!/bin/bash
#
# Need HOSTNAME within docker-compose for host-specific path to env file.
# export HOSTNAME
export HOSTNAME

COMPOSE_FILE="docker-compose.yml"
if [ ${HOSTNAME} = "nusa" ]
then
	COMPOSE_FILE="docker-compose-local.yml"
fi

docker-compose -f ${COMPOSE_FILE} rm --force --stop


