# Sensor Observation Service - SOS

This service configures and runs 
an [OGC SOS](http://www.opengeospatial.org/standards/sos) server using 
a Docker Image that embeds the [52North SOS Server](https://github.com/52North/SOS).

## Setup (Once)

Setup PG database schema once using [sos-clear.sh](config/sos-clear.sh).

Further configuration, see [config dir](config).

The following configuration files are relevant:

* SOS (server): [settings.json](config/settings.json).
* jsclient (viewer): [settings.json](config/jsclient/settings.json).

A sqlite DB contains all settings and is best copied from 
a previous SOS instance `/var/smartem/data/sos52n/configuration.db`.

## Running

Use the command ./run.sh

## Links

* SOS Standard - http://www.opengeospatial.org/standards/sos
* 52North SOS - https://52north.org/research/research-labs/sensor-web/


