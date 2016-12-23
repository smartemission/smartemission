# ETL - Extract, Transform, Load for sensor data

Sources for ETL of Smart Emission project Nijmegen.

Uses host-specific variables for databases, passwords etc (not in GitHub).

All ETL is developed using [Stetl](http://stetl.org).

Each Stetl Config file (`.cfg`) describes an ETL process. `.sh` files invoke the ETL processes.
Additional Python files implement specific ETL modules not defined
in the Stetl Framework.

All ETL processes are invoked using the same [Stetl Docker image](../docker/stetl/Dockerfile) and
scheduled via `cron`: [cronfile.txt](../platform/cronfile.txt)

The main ETL is multi-step as follows.

## Step 1: Fetching from RAW Sensor remote API

The following ETL configs/processes:

- Harvester: get all raw timeseries sensor-values from the [Whale API](../docs/specs/rawsensor-api/rawsensor-api.txt) for all devices [harvester.cfg](harvester.cfg)

As a result this raw sensor-data is stored in PostGIS [db-schema-raw.sql](db/db-schema-raw.sql). 
The Raw Data fetched via the Harvester is 
further processed in Step 2 Refiner.

## Step 2: Refiner

In this step all raw harvested timeseries data is "refined". Refinement involves the following:

- validation: remove outliers (pre and post)
- conversion: convert raw sensor values to standard units (e.g. temperature milliKelvin to degree Celsius)
- calibration: calibrate raw sensor gas-values to standard units using ANN (e.g. resistance/Ohm to AQ ug/m3 concentration)
- aggregation: make hourly average values for each sensor (''uurwaarden'')

See [refiner.cfg](refiner.cfg) and [refiner.py](refiner.py).
In particular the above steps are driven from the [sensordefs.py](sensordefs.py).
ANN calibration is implemented under [calibration](calibration).

As a result of this step, sensor-data timeseries (hour-values) are
stored in PostGIS [db-schema-refined.sql](db/db-schema-refined.sql). 

## Step 3: Publisher

In this step all refined/aggregated timeseries data is published to various IoT/SWE services. 
The following publishers are present:

- SOSPublisher - publish to a remote SOS via SOS-T(ransactional) protocol [sospublisher.cfg](sospublisher.cfg)
- STAPublisher - publish to a remote SensorThings API via REST [stapublisher.cfg](stapublisher.cfg) (31.10.16: work in progress)

All publication/output ETL uses Jinja2 templates with parameter substitution, e.g. [sostemplates](sostemplates) for SOS
and [statemplates](statemplates) for STA. 

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

In order to collect reference data and generate the ANN Calibration Estimator, 
three additional ETL processes have been added later in the project (dec 2016):

- [Extractor](extractor.cfg): to extract raw (Jose) Sensor Values from the Harvested (Step 1) RawDBInput into InfluxDB
- [Harvester_RIVM](harvester_rivm.cfg): to extract calibrated gas samples (hour averages) from RIVM LML SOS into InfluxDB
- [Calibrator](calibrator.cfg): to read/merge RIVM and Jose values from InfluxDB to create the ANN Estimator object (pickled)
 