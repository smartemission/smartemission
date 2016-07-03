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
  device_name character varying (32),
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

-- Stations
DROP VIEW IF EXISTS smartem_rt.stations CASCADE;
CREATE VIEW smartem_rt.stations AS
  SELECT DISTINCT on (d.device_id) d.gid, d.device_id, d.device_name, d.point, d.altitude, d.value_stale, d.time as last_update, ST_X(point) as lon, ST_Y(point) as lat  FROM smartem_rt.last_device_output as d order by d.device_id;

-- Alle Laatste Metingen
DROP VIEW IF EXISTS smartem_rt.v_last_measurements;
CREATE VIEW smartem_rt.v_last_measurements AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id,
    ST_X(point) as lon, ST_Y(point) as lat, EXTRACT(epoch from time ) AS timestamp
  FROM smartem_rt.last_device_output WHERE value_stale = 0 ORDER BY name ASC;

-- Laatste Metingen per Component
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO2;
CREATE VIEW smartem_rt.v_last_measurements_CO2 AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'co2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO;
CREATE VIEW smartem_rt.v_last_measurements_CO AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'co' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO_raw;
CREATE VIEW smartem_rt.v_last_measurements_CO_raw AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'coraw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2;
CREATE VIEW smartem_rt.v_last_measurements_NO2 AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2_raw;
CREATE VIEW smartem_rt.v_last_measurements_NO2_raw AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no2raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3;
CREATE VIEW smartem_rt.v_last_measurements_O3 AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'o3' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3_raw;
CREATE VIEW smartem_rt.v_last_measurements_O3_raw AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 's_o3raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_temperature;
CREATE VIEW smartem_rt.v_last_measurements_temperature AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'temperature' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_humidity;
CREATE VIEW smartem_rt.v_last_measurements_humidity AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'humidity' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_barometer;
CREATE VIEW smartem_rt.v_last_measurements_barometer AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'pressure' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_avg;
CREATE VIEW smartem_rt.v_last_measurements_audio_max AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'noiseavg' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_avg_level;
CREATE VIEW smartem_rt.v_last_measurements_audio_avg AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value as sample_value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'noiseavglevel' ORDER BY device_id, gid DESC;

