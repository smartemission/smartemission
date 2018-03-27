#!/bin/bash
#
# docker stop gost

# Need HOSTNAME within docker-compose for host-specific path to env file.
export HOSTNAME
docker-compose rm --force --stop
