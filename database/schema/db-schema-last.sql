-- Database defs for last values of Smart Emission data
ALTER DATABASE gis SET timezone TO 'Europe/Amsterdam';
ALTER DATABASE postgres SET timezone TO 'Europe/Amsterdam';

DROP SCHEMA IF EXISTS smartem_rt CASCADE;
CREATE SCHEMA smartem_rt;

-- Raw device realtime output table - data one2one from rawsensor api
DROP TABLE IF EXISTS smartem_rt.last_device_output CASCADE;
CREATE TABLE smartem_rt.last_device_output (
  gid serial,
  unique_id character varying,
  insert_time timestamp with time zone default current_timestamp,
  device_id integer,
  device_name character varying,
  device_meta character varying,
  sensor_meta character varying,
  name character varying,
  label character varying,
  unit  character varying,
  time timestamp with time zone,
  value_raw integer,
  value_stale integer,
  value real,
  altitude integer default 0,
  point geometry(Point,4326),
  PRIMARY KEY (gid)
) WITHOUT OIDS;

DROP INDEX IF EXISTS last_device_output_uid_idx;
CREATE UNIQUE INDEX last_device_output_uid_idx ON smartem_rt.last_device_output USING btree (unique_id) ;
DROP INDEX IF EXISTS last_device_output_geom_idx;
CREATE INDEX last_device_output_geom_idx ON smartem_rt.last_device_output USING gist (point);

-- VIEWS --

-- All Stations
DROP VIEW IF EXISTS smartem_rt.stations CASCADE;
CREATE VIEW smartem_rt.stations AS
  SELECT DISTINCT on (d.device_id)
    d.gid, d.device_id as device_id,
    CASE
     WHEN d.device_id > 99999999
       THEN
         d.device_id%100000
       ELSE
        d.device_id%10000
    END as device_subid,
    CASE
     WHEN d.device_id > 99999999
       THEN
         d.device_id/100000
       ELSE
        d.device_id/10000
    END as project_id,
    d.device_name, d.device_meta, d.point, d.altitude, d.value_stale,
    d.time as last_update, ST_X(point) as lon, ST_Y(point) as lat
  FROM smartem_rt.last_device_output as d order by d.device_id;

--
-- LAST MEASUREMENTS
--

-- Alle Laatste Metingen
DROP VIEW IF EXISTS smartem_rt.v_last_measurements;
CREATE VIEW smartem_rt.v_last_measurements AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id,
    ST_X(point) as lon, ST_Y(point) as lat, EXTRACT(epoch from time ) AS timestamp
  FROM smartem_rt.last_device_output WHERE value_stale = 0 ORDER BY name ASC;

-- Laatste Metingen per Component
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO2;
CREATE VIEW smartem_rt.v_last_measurements_CO2 AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'co2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO;
CREATE VIEW smartem_rt.v_last_measurements_CO AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'co' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO_raw;
CREATE VIEW smartem_rt.v_last_measurements_CO_raw AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'coraw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO;
CREATE VIEW smartem_rt.v_last_measurements_NO AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO_raw;
CREATE VIEW smartem_rt.v_last_measurements_NO_raw AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'noraw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2;
CREATE VIEW smartem_rt.v_last_measurements_NO2 AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2_raw;
CREATE VIEW smartem_rt.v_last_measurements_NO2_raw AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no2raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3;
CREATE VIEW smartem_rt.v_last_measurements_O3 AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'o3' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3_raw;
CREATE VIEW smartem_rt.v_last_measurements_O3_raw AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'o3raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_PM10;
CREATE VIEW smartem_rt.v_last_measurements_PM10 AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'pm10' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_PM25;
CREATE VIEW smartem_rt.v_last_measurements_PM25 AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'pm2_5' ORDER BY device_id, gid DESC;

-- DROP VIEW IF EXISTS smartem_rt.v_last_measurements_PM1;
-- CREATE VIEW smartem_rt.v_last_measurements_PM1 AS
--   SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
--     name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
--   FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'pm1' ORDER BY device_id, gid DESC;
--
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_temperature;
CREATE VIEW smartem_rt.v_last_measurements_temperature AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'temperature' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_humidity;
CREATE VIEW smartem_rt.v_last_measurements_humidity AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'humidity' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_barometer;
CREATE VIEW smartem_rt.v_last_measurements_barometer AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'pressure' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_avg;
CREATE VIEW smartem_rt.v_last_measurements_noise_avg AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'noiseavg' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_level_avg;
CREATE VIEW smartem_rt.v_last_measurements_noise_level_avg AS
  SELECT device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'noiselevelavg' ORDER BY device_id, gid DESC;

--
-- CURRENT MEASUREMENTS
--

-- All Current Measurements (last hour)
DROP VIEW IF EXISTS smartem_rt.v_cur_measurements CASCADE;
CREATE VIEW smartem_rt.v_cur_measurements AS
  SELECT gid, unique_id, device_id, device_name, device_meta, sensor_meta,label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, altitude,
    ST_X(point) as lon, ST_Y(point) as lat, EXTRACT(epoch from time ) AS timestamp
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND time > now() - interval '120 minutes' ORDER BY device_id ASC;

-- Current Measurements per Component
DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_CO2;
CREATE VIEW smartem_rt.v_cur_measurements_CO2 AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'co2';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_CO;
CREATE VIEW smartem_rt.v_cur_measurements_CO AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'co';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_NO;
CREATE VIEW smartem_rt.v_cur_measurements_NO AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'no';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_NO2;
CREATE VIEW smartem_rt.v_cur_measurements_NO2 AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'no2';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_O3;
CREATE VIEW smartem_rt.v_cur_measurements_O3 AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'o3';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_PM10;
CREATE VIEW smartem_rt.v_cur_measurements_PM10 AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'pm10';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_PM25;
CREATE VIEW smartem_rt.v_cur_measurements_PM25 AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'pm2_5';

-- DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_PM1;
-- CREATE VIEW smartem_rt.v_cur_measurements_PM1 AS
--   SELECT *
--   FROM smartem_rt.v_cur_measurements WHERE name = 'pm1' ORDER BY device_id, gid DESC;
--
DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_temperature;
CREATE VIEW smartem_rt.v_cur_measurements_temperature AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'temperature';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_humidity;
CREATE VIEW smartem_rt.v_cur_measurements_humidity AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'humidity';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_barometer;
CREATE VIEW smartem_rt.v_cur_measurements_barometer AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'pressure';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_noise_avg;
CREATE VIEW smartem_rt.v_cur_measurements_noise_avg AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'noiseavg';

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_noise_level_avg;
CREATE VIEW smartem_rt.v_cur_measurements_noise_level_avg AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'noiselevelavg';

-- All Current/Active Stations
DROP VIEW IF EXISTS smartem_rt.v_cur_stations CASCADE;
CREATE VIEW smartem_rt.v_cur_stations AS
  SELECT DISTINCT on (d.device_id)
    d.gid, d.device_id as device_id,
    CASE
     WHEN d.device_id > 99999999
       THEN
         d.device_id%100000
       ELSE
        d.device_id%10000
    END as device_subid,
    CASE
     WHEN d.device_id > 99999999
       THEN
         d.device_id/100000
       ELSE
        d.device_id/10000
    END as project_id,
    d.device_name, d.device_meta,
    d.point, d.altitude, d.value_stale, d.sample_time as last_update, lon, lat
  FROM smartem_rt.v_cur_measurements as d order by d.device_id;
