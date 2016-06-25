# ETL - Extract, Transform, Load for sensor data

Sources for ETL of Smart Emission project Nijmegen.

Uses host-specific variables for databases, passwords etc.

Most ETL is developed using Stetl: http://stetl.org

All ETL processes are scheduled via `cron`: [../platform/cronfile.txt](cronfile.txt)

## Fetching from RAW Sensor remote API

Two ETL configs/processes:

- Last: get and convert last sensor-values for all devices: `last.cfg`
- Harvester: get all raw timeseries sensor-values for all devices `harvester.cfg`

As a result sensor-data is stored in PostGIS. The Raw Data fetched via the Harvester is 
further processed. See next.

## Refiner

In this step all raw harvested timeseries data is "refined". This involves the following:

- calibration: convert raw sensor values (like resistance/Ohm) to AQ concentration
- aggregation: make average values for each sensor


