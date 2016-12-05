This runs the InfluxDB service.
See https://www.influxdata.com
The Docker image comes via:
https://hub.docker.com/_/influxdb/

InfluxDB is not perse a component of the SE platform but could be in the future. 
For now mainly used to test the EU JRC AirSensEUR AQ Sensor: http://www.airsenseur.org.

Enabled Auth:

https://docs.influxdata.com/influxdb/v1.1/query_language/authentication_and_authorization/#authorization

sudo docker exec -it influxdb  bash
influx -username <user> -password <pass>

https://docs.influxdata.com/influxdb/v1.1/introduction/getting_started/#creating-a-database
create database airsenseur

Create DB user and give access to DB
CREATE USER <username> WITH PASSWORD '<password>'
GRANT ALL ON airsenseur TO <username>


