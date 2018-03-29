#!/bin/bash
#
# Run the SOS Emu
#

# Need HOSTNAME within docker-compose for host-specific path to env file.
export HOSTNAME

docker-compose rm --force --stop
docker-compose up -d
