 -- Database defs for refined timeseries values of Smart Emission data

DROP SCHEMA IF EXISTS smartem_refined CASCADE;
CREATE SCHEMA smartem_refined;

-- Raw device realtime output table - data one2one from rawsensor api
DROP TABLE IF EXISTS smartem_refined.timeseries CASCADE;
CREATE TABLE smartem_refined.timeseries (
  gid serial,
  gid_raw integer, -- gid of the harvested raw data record
  insert_time timestamp with time zone default current_timestamp,
  device_id integer,
  device_meta character varying default 'jose-1',
  sensor_meta character varying default 'unknown',
  name character varying,
  label character varying,
  unit  character varying,
  time timestamp with time zone,
  day integer not null,
  hour integer not null,
  value_min integer,
  value_max integer,
  value_raw integer,
  value integer,
  sample_count integer,
  altitude integer default 0,
  point geometry(Point,4326),
  PRIMARY KEY (gid)
) WITHOUT OIDS;

DROP INDEX IF EXISTS timeseries_geom_idx;
CREATE INDEX timeseries_geom_idx ON smartem_refined.timeseries USING gist (point);

-- See https://stackoverflow.com/questions/32042152/add-an-index-to-a-timestamp-with-time-zone
DROP INDEX IF EXISTS timeseries_time_idx;
CREATE INDEX timeseries_time_idx ON smartem_refined.timeseries(time);

-- ETL progress tabel, tracks last inserted timeseries (from raw sensor db) per device.
DROP TABLE IF EXISTS smartem_refined.refiner_progress CASCADE;
CREATE TABLE smartem_refined.refiner_progress (
  gid serial,
  insert_time timestamp with time zone default current_timestamp,
  gid_raw integer not null,
  device_id integer not null,
  day integer not null,
  hour integer not null,
  PRIMARY KEY (gid)
) WITHOUT OIDS;

-- TRIGGER to update checkpointing by storing last day/hour for each device
-- Thus the Harvester always knows where to start from when running
CREATE OR REPLACE FUNCTION smartem_refined.progress_update() RETURNS TRIGGER AS $refiner_progress_update$
  BEGIN
        --
        -- Set the progress for the device id to the last day+hour harvested
        -- make use of the special variable TG_OP to work out the operation.
        --

        IF (TG_OP = 'INSERT') THEN
          -- Delete possibly existing entry for device
          DELETE FROM smartem_refined.refiner_progress; -- WHERE device_id = NEW.device_id;

          -- Always insert new entry for device with latest harvested day/hour
          INSERT INTO smartem_refined.refiner_progress (gid_raw, device_id, day, hour)
              VALUES (NEW.gid_raw, NEW.device_id, NEW.day, NEW.hour);
        END IF;

        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;

$refiner_progress_update$ LANGUAGE plpgsql;

--exec
DROP TRIGGER IF EXISTS refiner_progress_update ON smartem_refined.timeseries;

--exec
CREATE TRIGGER refiner_progress_update AFTER INSERT ON smartem_refined.timeseries
    FOR EACH ROW EXECUTE PROCEDURE smartem_refined.progress_update();

-- ETL progress table, tracks Publisher ETL processing ("worker") 
-- For each worker tracks last processed record id (gid).
DROP TABLE IF EXISTS smartem_refined.etl_progress CASCADE;
CREATE TABLE smartem_refined.etl_progress (
  gid serial,
  worker character varying (25),
  source_table  character varying (25),
  last_gid  integer,
  last_update timestamp,
  PRIMARY KEY (gid)
);

-- Define workers
INSERT INTO smartem_refined.etl_progress (worker, source_table, last_gid, last_update)
        VALUES ('sospublisher', 'timeseries', -1, current_timestamp);

INSERT INTO smartem_refined.etl_progress (worker, source_table, last_gid, last_update)
        VALUES ('stapublisher', 'timeseries', -1, current_timestamp);

-- VIEWS --

-- Stations
DROP VIEW IF EXISTS smartem_refined.stations CASCADE;
CREATE VIEW smartem_refined.stations AS
  SELECT DISTINCT on (d.device_id) d.gid, d.device_id, d.device_meta, d.point, d.altitude, d.time as last_update, ST_X(point) as lon, ST_Y(point) as lat  FROM smartem_refined.timeseries as d order by d.device_id;

-- Alle Laatste Metingen
DROP VIEW IF EXISTS smartem_refined.v_timeseries;
CREATE VIEW smartem_refined.v_timeseries AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw,
    ST_X(point) as lon, ST_Y(point) as lat, EXTRACT(epoch from time ) AS timestamp
  FROM smartem_refined.timeseries ORDER BY name ASC;

 -- Laatste Metingen per Component
DROP VIEW IF EXISTS smartem_refined.v_timeseries_CO2;
CREATE VIEW smartem_refined.v_timeseries_CO2 AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'co2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_CO;
CREATE VIEW smartem_refined.v_timeseries_CO AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'co' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_CO_raw;
CREATE VIEW smartem_refined.v_timeseries_CO_raw AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'coraw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_NO2;
CREATE VIEW smartem_refined.v_timeseries_NO2 AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'no2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_NO2_raw;
CREATE VIEW smartem_refined.v_timeseries_NO2_raw AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'no2raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_O3;
CREATE VIEW smartem_refined.v_timeseries_O3 AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'o3' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_O3_raw;
CREATE VIEW smartem_refined.v_timeseries_O3_raw AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'o3raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_PM10;
CREATE VIEW smartem_refined.v_timeseries_PM10 AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'pm10' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_PM25;
CREATE VIEW smartem_refined.v_timeseries_PM25 AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'pm2_5' ORDER BY device_id, gid DESC;

-- DROP VIEW IF EXISTS smartem_refined.v_timeseries_PM1;
-- CREATE VIEW smartem_refined.v_timeseries_PM1 AS
--   SELECT device_id, device_meta, sensor_meta, name, label,
--     unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
--   FROM smartem_refined.timeseries WHERE name = 'pm1' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_temperature;
CREATE VIEW smartem_refined.v_timeseries_temperature AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'temperature' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_humidity;
CREATE VIEW smartem_refined.v_timeseries_humidity AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'humidity' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_barometer;
CREATE VIEW smartem_refined.v_timeseries_barometer AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'pressure' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_noise_avg;
CREATE VIEW smartem_refined.v_timeseries_noise_avg AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'noiseavg' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_noise_level_avg;
CREATE VIEW smartem_refined.v_timeseries_noise_level_avg AS
  SELECT device_id, device_meta, sensor_meta, name, label,
    unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
  FROM smartem_refined.timeseries WHERE name = 'noiselevelavg' ORDER BY device_id, gid DESC;


