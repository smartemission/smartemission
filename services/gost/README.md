# SensorThings API - GOST

This service configures and runs 
a [SensorThings API](http://ogc-iot.github.io/ogc-iot-api/api.html) server using 
the Docker container for [Geodan GOST](https://www.gostserver.xyz).

## Database

Setup once using [config/gost-init-db.sh](config/gost-init-db.sh).

## Configuration

See [gost_configuration.md](https://github.com/gost/docs/blob/master/gost_configuration.md).

Uses host-specific config vars. `HOSTNAME` needs to be exported for `docker-compose`
to find the env file specific to the host.

## Running

Use the command `./run.sh` and `./stop.sh` or

```
export HOSTNAME
docker-compose up

```

## Links

* GOST - https://github.com/gost/server
* GOST DB - https://github.com/gost/gost-db
