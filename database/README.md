# Smart Emission Data Platform - Databases

Below all [schemas](schema) and [utilities](util) for managing all databases.

The SE Platform uses both PostgreSQL/PostGIS and InfluxDB.

## PostgreSQL

A single database named `gis` is used. 
It runs via the [Postgis Docker image](../docker/postgis/Dockerfile) and [service](../services/postgis).
The following schemas are defined:

* [smartem_calibrated](schema/db-schema-calibrate.sql): stores ANN learning result and ANN calibration state
* [smartem_extracted](schema/db-schema-extract.sql): stores progress state for raw gas value extraction into InfluxDB
* [smartem_harvest_rivm](schema/db-schema-harvest-rivm.sql): ditto for harvesting progress from RIVM SOS into InfluxDB
* [smartem_meta](schema/db-schema-meta.sql): NOT YET IN USE - first throw at keeping sensor and project metadata
* [smartem_raw](schema/db-schema-raw.sql): holds all harvested raw sensor data
* [smartem_refined](schema/db-schema-refined.sql): holds all refined/processed (via ETL Refiner) sensor data
* [smartem_rt](schema/db-schema-last.sql): rt=real-time, holds all last/realtime sensor data
* [sos52n1](../services/sos52n/config/db-init.sql): SOS database, created/maintained by 52North SOS server
* [v1](../services/gost/config/gost-init-db.sql): SensorThings API database, created/maintained by Geodan GOST server 

## InfluxDB

The following databases are defined, as initialized via [db-init-influxdb.sh](db-init-influxdb.sh).
The [InfluxDB server](../services/influxdb) runs using the standard InfluxDB Docker image.

### Smart Emission Influx Database

Used for ANN calibration learning process raw data and reference (RIVM) gas-data inputs, plus
holds the refined gas values from the Refiner ETL process.

### AirSensEUR Influx Database

Used for AirSensEUR sensor devices. 
Each ASE device publishes to a separate InfluxDB Measurements table. 
This data is harvested into the SE Raw database for further standard ETL processing
and services publication.







