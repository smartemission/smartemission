# ETL - Extract, Transform, Load for sensor data

Sources for ETL of Smart Emission project Nijmegen.

Uses host-specific variables for databases, passwords etc.

All ETL is developed using Stetl: http://stetl.org

Each Stetl Config file (.cfg) describes an ETL process. .sh files invoke the ETL processes.
Additional Python files implement specific ETL modules not defined
in the Stetl Framework.

All ETL processes are invoked using the same [Stetl Docker image](../docker/stetl/Dockerfile) and
scheduled via `cron`: [cronfile.txt](../platform/cronfile.txt)

The ETL is multi-step as follows.

## Step 1: Fetching from RAW Sensor remote API

The following ETL configs/processes:

- Harvester: get all raw timeseries sensor-values for all devices [harvester.cfg]

As a result sensor-data is stored in PostGIS. The Raw Data fetched via the Harvester is 
further processed. See next.

## Step 2: Refiner

In this step all raw harvested timeseries data is "refined". Refinement involves the following:

- validation: remove outliers (pre and post)
- conversion: convert raw sensor values to standard units (e.g. temperature milliKelvin to degree Celsius)
- calibration: calibrate raw sensor gas-values to standard units using ANN (e.g. resistance/Ohm to AQ ug/m3 concentration)
- aggregation: make hourly average values for each sensor (''uurwaarden'')


## Step 3: Publisher

In this step all refined/aggregated timeseries data is published to various IoT/SWE services. 
The following publishers are present:

- SOSPublisher - publish to a remote SOS via SOS-T(ransactional) protocol [sospublisher.cfg]
- STAPublisher - publish to a remote SensorThings API via REST [stapublisher.cfg] (31.10.16: work in progress)

All publication/output ETL uses Jinja2 templates with parameter substitution, e.g. [sostemplates] for SOS. 

NB publication to WFS and WMS is not explicitly required: these services directly
use the timeseries refined tables and Postgres VIEWs from Step 2.

## Last Values

This step is special: it is a pass-through from the Raw Sensor API to a single
table with (refined) last values for all sensors for the SOS emulation API (sosemu).
This ETL process originated historically as no SOS and STA was initially available
but the project needed to develop the SmartApp with last values.

- Last: get and convert last sensor-values for all devices: [last.cfg]

