# InfluxDB Server

This runs the InfluxDB service as a Docker container. See https://www.influxdata.com
The Docker image comes from https://hub.docker.com/_/influxdb/

InfluxDB is not perse a component of the SE platform but could be in the future. 
For now mainly used to test the EU JRC AirSensEUR AQ Sensor: http://www.airsenseur.org.

## Authorization

See https://docs.influxdata.com/influxdb/v1.1/query_language/authentication_and_authorization/#authorization

We need admin user. All below via `influx` CLI.

```
sudo docker exec -it influxdb  bash
influx -username <user> -password <pass>
```

Creating a database. See https://docs.influxdata.com/influxdb/v1.1/introduction/getting_started/#creating-a-database

```
CREATE DATABASE airsenseur
```

Create DB user and give access to DB

```
CREATE USER <username> WITH PASSWORD '<password>'
GRANT ALL ON airsenseur TO <username>
```

## Writing Data

See https://docs.influxdata.com/influxdb/v1.1/guides/writing_data/
Writing data, for example for raw Josene Sensor data could be:

```
curl -i -XPOST 'http://localhost:8086/write?db=smartemraw' --data-binary 'joseraw,station=19,component=no2raw value=12345 1434055562000000000'
```

or multiple measurements, each on a new line:

```
curl -i -XPOST 'http://localhost:8086/write?db=smartemraw' --data-binary 'joseraw,station=19,component=no2raw value=12345 1434055562000000000
joseraw,station=23,component=temperature value=18 1434055562000000000
joseraw,station=19,component=o3raw value=12345 1434055562000000000'
```
