# SensorThings API - GOST

This service configures and runs 
a [SensorThings API](http://ogc-iot.github.io/ogc-iot-api/api.html) server using 
the Docker container for [Geodan GOST](https://www.gostserver.xyz).

## Database

Setup once using [config/gost-init-db.sh](config/gost-init-db.sh).

## Configuration

See [gost_configuration.md](https://github.com/gost/docs/blob/master/gost_configuration.md).

The following configuration parameters can be 
overruled from the following environment variables:

* db: gost_db_host, gost_db_database, gost_db_port, gost_db_user, gost_db_password.
* mqtt: gost_mqtt_host, gost_mqtt_port
* server: gost_server_host, gost_server_port, gost_server_external_uri, gost_client_content

## Running

Use the command ./run.sh

## Links

* GOST - https://github.com/gost/server
* GOST DB - https://github.com/gost/gost-db
