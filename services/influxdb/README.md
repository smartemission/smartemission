# InfluxDB Server

This runs the InfluxDB service as a Docker container. See https://www.influxdata.com:

> InfluxDB is an open source database written in Go specifically to handle time 
> series data with high availability and high performance requirements. 
> InfluxDB installs in minutes without external dependencies, yet is 
> flexible and scalable enough for complex deployments.

The Docker image comes from https://hub.docker.com/_/influxdb/

## Use in SE

InfluxDB is used in the SE platform initially for storing time-series for kalibration ANN learning
and to test the EU JRC AirSensEUR AQ Sensor: http://www.airsenseur.org and possibly other attached sensors.
InfluxDB will in time become a central part of the SE platform. 

## Docker

Docker is used to deploy/run InfluxDB. See the [run.sh script](run.sh).

The Docker container will expose the InfluxDB ports (8086 and 8083). It makes the following
Docker-internal directories available to your local machine: 

- config: `/etc/influxdb/influxdb.conf` to [./config/influxdb.conf](config/influxdb.conf)
- data: `/var/lib/influxdb` to `/var/smartem/data/influxdb` 
- logs: `/var/log/influxdb` to `/var/smartem/log/influxdb` 

You may edit the [./config/influxdb.conf](config/influxdb.conf) for your local machine.
Enable authentication by setting the auth-enabled option to true in the ``[http]`` 
section of the [configuration file](config/influxdb.conf).

Database initialization: tbs.

Run `/usr/bin/influx` command as follows:

```
sudo docker run --rm --net=container:influxdb -it influxdb influx -host localhost
```

## Visualization

InfluxDB is closely integrated with Grafana (http://grafana.org). See the [Grafana Service](../grafana) in SE platform.

## Authorization

See https://docs.influxdata.com/influxdb/v1.1/query_language/authentication_and_authorization/#authorization

We use two types of users: a global `admin` user and a per-DB user.

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

## Query Data

See https://docs.influxdata.com/influxdb/v1.1/guides/querying_data/

To select all `no2` from `measurement` `joseraw`:

```
SELECT * FROM joseraw WHERE component = 'no2'
```
            
## Delete Data

To delete from `measurement` `joseraw`:

```
DELETE FROM joseraw WHERE time > '1970-01-01'
```

## Geospatial Data

While InfluxDB has no specific geospatial support, a common way to tag measurements with lat/lon values is
via Geohash (https://en.wikipedia.org/wiki/Geohash). The common Python module is https://github.com/vinsci/geohash.
Tools like Grafana can interpret geohashes in Dashboards when the tag name is `geohash`.

A line would be like:

```
joseraw,station=70,component=pressure,geohash=u1hhc432rtwb value=1006 1476435600000000000
```
