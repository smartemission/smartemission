-- 16.jan.2018

DROP INDEX IF EXISTS timeseries_day_hour_idx;
CREATE INDEX timeseries_day_hour_idx ON smartem_raw.timeseries USING btree (day, hour);

-- Updates to support more sensor types, default is Josene
ALTER TABLE smartem_raw.timeseries  ADD COLUMN IF NOT EXISTS
  device_type character varying not null default 'jose';
ALTER TABLE smartem_raw.timeseries  ADD COLUMN IF NOT EXISTS
  device_version character varying not null default '1';


-- TRIGGER to update checkpointing by storing last day/hour for each device
-- Thus the Harvester always knows where to start from when running
CREATE OR REPLACE FUNCTION smartem_raw.harvester_progress_update() RETURNS TRIGGER AS $harvester_progress_update$
  BEGIN
        --
        -- Set the progress for the device id to the last day+hour harvested
        -- make use of the special variable TG_OP to work out the operation.
        --

        IF ((TG_OP = 'INSERT') AND (NEW.complete = TRUE)) THEN
          -- Delete possibly existing entry for device
          DELETE FROM smartem_raw.harvester_progress WHERE device_id = NEW.device_id;

          -- Always insert new entry for device with latest harvested day/hour
          INSERT INTO smartem_raw.harvester_progress (unique_id, device_id, day, hour)
              VALUES (NEW.unique_id, NEW.device_id, NEW.day, NEW.hour);
        END IF;

        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;

$harvester_progress_update$ LANGUAGE plpgsql;

--exec
DROP TRIGGER IF EXISTS harvester_progress_update ON smartem_raw.timeseries;

--exec
CREATE TRIGGER harvester_progress_update AFTER INSERT ON smartem_raw.timeseries
    FOR EACH ROW EXECUTE PROCEDURE smartem_raw.harvester_progress_update();



-- VIEWs

-- Raw data of the current hour
DROP VIEW IF EXISTS smartem_raw.timeseries_current CASCADE;
CREATE VIEW smartem_raw.timeseries_current AS
  SELECT * from smartem_raw.timeseries
  WHERE day = cast(to_char(current_timestamp AT TIME ZONE 'UTC', 'YYYYMMDD') AS INT) AND
        hour = cast(to_char(current_timestamp AT TIME ZONE 'UTC', 'HH24') AS INT) ORDER BY device_id;

-- Raw data last produced
DROP VIEW IF EXISTS smartem_raw.timeseries_last CASCADE;
CREATE VIEW smartem_raw.timeseries_last AS
  SELECT * from smartem_raw.timeseries
  WHERE complete = FALSE  ORDER BY device_id;

ALTER TABLE smartem_refined.timeseries  ADD COLUMN IF NOT EXISTS
  device_meta character varying default 'jose-1';
ALTER TABLE smartem_refined.timeseries  ADD COLUMN IF NOT EXISTS
  sensor_meta character varying default 'unknown';

UPDATE smartem_refined.timeseries
  SET sensor_meta = (case
        WHEN name = 'temperature' then 'temp-S12'
        WHEN name = 'humidity' then 'humid-S13'
        WHEN name = 'pressure' then 'press-S16'
        WHEN name = 'co2' then 'co2-S23'
        WHEN name = 'co' then 'co-S26'
        WHEN name = 'coraw' then 'co-S26'
        WHEN name = 'no2' then 'no2-S27'
        WHEN name = 'no2raw' then 'no2-S27'
        WHEN name = 'o3' then 'o3-S28'
        WHEN name = 'o3raw' then 'o3-S28'
        WHEN name = 'pm10' then 'pm10-S29'
        WHEN name = 'pm2_5' then 'pm2_5-S2A'
        WHEN name = 'noiseavg' then 'au-V30_V3F'
        WHEN name = 'noiselevelavg' then 'au-V30_V3F'

        ELSE 'UNKNOWN'
      end);


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

DROP VIEW IF EXISTS smartem_refined.v_timeseries_PM2_5;
CREATE VIEW smartem_refined.v_timeseries_PM2_5 AS
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


