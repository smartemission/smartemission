# ETL - Extract, Transform, Load for sensor data

Sources for ETL of the Smart Emission Platform. Originally this ETL was developed
for the Smart Emission Project Nijmegen and the Intemo Josene Sensor Device. 
As to accommodate other sensor devices like the [EU JRC AirSensEUR](http://www.airsenseur.org), the ETL-framework
has been generalized. 

Uses host-specific variables for databases, passwords etc (not stored in GitHub).

All ETL is developed using [Stetl](http://stetl.org). Stetl is a Python framework and programming model for any ETL
process. The essence of Stetl is that each ETL process is a chain of linked Input, Filters and Output Python classes
specified in a Stetl Config File.

Each Stetl Config file (`.cfg`) describes an ETL process. `.sh` files invoke the ETL processes. Stetl is run via Docker.
Additional Python files implement specific ETL modules not defined
in the Stetl Framework and are available under the Python [smartem](smartem) package.

All ETL processes are invoked using the same [Stetl Docker image](../docker/stetl/Dockerfile) and
scheduled via `cron`: [cronfile.txt](../platform/cronfile.txt)

The main ETL is multi-step as follows.

## Step 1: Harvesters - Fetching raw sensor data

The SE ETL follows a "pull" model: raw sensor data is "harvested" from data collector servers and other sensor networks.

The following ETL configs/processes:

- Harvester Whale: get all raw timeseries sensor-values from the [Whale API](../docs/specs/rawsensor-api/rawsensor-api.txt) for Intemo Jose sensor devices, see [harvester_whale.cfg](harvester_whale.cfg)
- Harvester Influx: get all raw timeseries sensor-values from an InfluxDB, initially for AirSensEUR (ASE) devices, see [harvester_influx.cfg](harvester_influx.cfg)

As a result all raw sensor-data is stored in PostGIS using the schema [db-schema-raw.sql](db/db-schema-raw.sql). 
The Raw Data fetched via the Harvesters is further processed in Step 2 Refiner.

## Step 2: Refiners

In this step all raw harvested timeseries data is "refined". Refinement involves the following:

- validation: remove outliers (pre and post)
- conversion: convert raw sensor values to standard units (e.g. temperature milliKelvin to degree Celsius)
- calibration: calibrate raw sensor gas-values to standard units using ANN (e.g. resistance/Ohm to AQ ug/m3 concentration)
- aggregation: make hourly average values for each sensor (''uurwaarden'')

See [refiner.cfg](refiner.cfg) and [smartem/refiner](smartem/refiner).
In particular the above steps are driven from the type of sensor device.
The learning process for ANN calibration is implemented under [smartem/calibrator](smartem/calibrator).

As a result of this step, sensor-data timeseries (hour-values) are
stored in PostGIS [db-schema-refined.sql](db/db-schema-refined.sql) AND in InfluxDB. 

## Step 3: Publishers

In this step all refined/aggregated timeseries data is published to various IoT/SWE services. 
The following publishers are present:

- SOSPublisher - publish to a remote SOS via SOS-T(ransactional) protocol [sospublisher.cfg](sospublisher.cfg)
- STAPublisher - publish to a remote SensorThings API (STA) via REST [stapublisher.cfg](stapublisher.cfg) 

All publication/output ETL uses plain Python string templates (no need for Jinja2 yet) with parameter 
substitution, e.g. [smartem/publisher/sostemplates](smartem/publisher/sostemplates) for SOS and [smartem/publisher/statemplates](smartem/publisher/statemplates) for STA. 

NB publication to WFS and WMS is not explicitly required: these services directly
use the timeseries refined tables and Postgres VIEWs from Step 2.

## Last Values

This step is special: it is a pass-through from the Raw Sensor API to a single
table with (refined) last values for all sensors for the SOS emulation API (sosemu).
This ETL process originated historically as no SOS and STA was initially available
but the project needed to develop the SmartApp with last values.

- Last: get and convert last sensor-values for all devices: [last.cfg](last.cfg).

As a result this raw sensor-data is stored in PostGIS [db-schema-last.sql](db/db-schema-last.sql).
 
## Calibration

(Currently only for Intemo Josene devices)

In order to collect reference data and generate the ANN Calibration Estimator, 
three additional ETL processes have been added later in the project (dec 2016):

- [Extractor](extractor.cfg): to extract raw (Jose) Sensor Values from the Harvested (Step 1) RawDBInput into InfluxDB
- [Harvester_RIVM](harvester_rivm.cfg): to extract calibrated gas samples (hour averages) from RIVM LML SOS into InfluxDB

The above two datasets in InfluxDB are used to generate the ANN Calibration Estimator object by running the Calibrator
ETL process:

- [Calibrator](calibrator.cfg): to read/merge RIVM and Jose values from InfluxDB to create the ANN Estimator object (pickled)
 