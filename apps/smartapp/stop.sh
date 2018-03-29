#!/bin/bash

# Need HOSTNAME within docker-compose for host-specific path to env file.
export HOSTNAME

# stop
docker-compose rm --force --stop
