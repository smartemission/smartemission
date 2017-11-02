-- 28 oct 2017 - one time DB upgrade-needed for Smart City Living Lab

ALTER TABLE smartem_raw.timeseries  ALTER COLUMN unique_id TYPE character varying;
ALTER TABLE smartem_raw.harvester_progress  ALTER COLUMN unique_id TYPE character varying;

-- Drop de VIEWs eerst
DROP VIEW IF EXISTS smartem_rt.stations CASCADE;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO2;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO_raw;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2_raw;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3_raw;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_temperature;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_humidity;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_barometer;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_avg;
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_level_avg;


ALTER TABLE smartem_rt.last_device_output  ALTER COLUMN device_name TYPE character varying;

-- Herlaad VIEWs

-- Stations
DROP VIEW IF EXISTS smartem_rt.stations CASCADE;
CREATE VIEW smartem_rt.stations AS
  SELECT DISTINCT on (d.device_id) d.gid, d.device_id, d.device_name, d.point, d.altitude, d.value_stale, d.time as last_update, ST_X(point) as lon, ST_Y(point) as lat  FROM smartem_rt.last_device_output as d order by d.device_id;

-- Alle Laatste Metingen
DROP VIEW IF EXISTS smartem_rt.v_last_measurements;
CREATE VIEW smartem_rt.v_last_measurements AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id,
    ST_X(point) as lon, ST_Y(point) as lat, EXTRACT(epoch from time ) AS timestamp
  FROM smartem_rt.last_device_output WHERE value_stale = 0 ORDER BY name ASC;

-- Laatste Metingen per Component
DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO2;
CREATE VIEW smartem_rt.v_last_measurements_CO2 AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'co2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO;
CREATE VIEW smartem_rt.v_last_measurements_CO AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'co' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_CO_raw;
CREATE VIEW smartem_rt.v_last_measurements_CO_raw AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'coraw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2;
CREATE VIEW smartem_rt.v_last_measurements_NO2 AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no2' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_NO2_raw;
CREATE VIEW smartem_rt.v_last_measurements_NO2_raw AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'no2raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3;
CREATE VIEW smartem_rt.v_last_measurements_O3 AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'o3' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_O3_raw;
CREATE VIEW smartem_rt.v_last_measurements_O3_raw AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'o3raw' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_temperature;
CREATE VIEW smartem_rt.v_last_measurements_temperature AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'temperature' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_humidity;
CREATE VIEW smartem_rt.v_last_measurements_humidity AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'humidity' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_barometer;
CREATE VIEW smartem_rt.v_last_measurements_barometer AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'pressure' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_avg;
CREATE VIEW smartem_rt.v_last_measurements_noise_avg AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'noiseavg' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_rt.v_last_measurements_noise_level_avg;
CREATE VIEW smartem_rt.v_last_measurements_noise_level_avg AS
  SELECT device_id, device_name, label, unit,
    name, value_raw, value_stale, time AS sample_time, value, point, gid, unique_id
  FROM smartem_rt.last_device_output WHERE value_stale = 0 AND name = 'noiselevelavg' ORDER BY device_id, gid DESC;

