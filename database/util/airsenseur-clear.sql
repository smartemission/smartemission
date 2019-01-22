--
-- Clear and reset all AirSensEUR related data in PostGIS DBs (schemas)
--
-- # 1 delete ASE data harvested from smartem_raw.timeseries
-- # select count(gid) from smartem_raw.timeseries where device_id/10000 = 1182;
-- # DELETE FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;
-- # 2 reset harvester position to start of RIVM deployment (aug 1, 2018)
-- # UPDATE smartem_raw.harvester_progress SET day = 180801, hour = 1 WHERE device_id/10000 = 1182;
--
-- # 3 delete refined ASE data in smartem_refined.timeseries
-- # DELETE FROM smartem_refined.timeseries WHERE device_id/10000 = 1182;


-- Extra View NO Last Measurements
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

DROP VIEW IF EXISTS smartem_rt.v_cur_measurements_NO;
CREATE VIEW smartem_rt.v_cur_measurements_NO AS
  SELECT *
  FROM smartem_rt.v_cur_measurements WHERE name = 'no';

-- Extra View NO Refined Measurements
DROP VIEW IF EXISTS smartem_refined.v_timeseries_NO;
CREATE VIEW smartem_refined.v_timeseries_NO AS
 SELECT device_id, device_meta, sensor_meta, name, label,
   unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
 FROM smartem_refined.timeseries WHERE name = 'no' ORDER BY device_id, gid DESC;

DROP VIEW IF EXISTS smartem_refined.v_timeseries_NO_raw;
CREATE VIEW smartem_refined.v_timeseries_NO_raw AS
 SELECT device_id, device_meta, sensor_meta, name, label,
   unit, value, value_raw, value_min, value_max, time, day, hour, sample_count, point, gid, gid_raw
 FROM smartem_refined.timeseries WHERE name = 'noraw' ORDER BY device_id, gid DESC;

-- 1. Delete Harvested data from InfluxDB and
SELECT count(gid) FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;
DELETE FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;
SELECT count(gid) FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;

-- 2. Reset Harvester State to start of calibration period (1.8.2018)
-- UPDATE smartem_raw.harvester_progress SET day = 20180801, hour = 1 WHERE device_id/10000 = 1182;
UPDATE smartem_raw.harvester_progress SET day = 20180801, hour = 1 WHERE device_id = 11820001;
UPDATE smartem_raw.harvester_progress SET day = 20180801, hour = 1 WHERE device_id = 11820002;
UPDATE smartem_raw.harvester_progress SET day = 20180801, hour = 1 WHERE device_id = 11820003;
UPDATE smartem_raw.harvester_progress SET day = 20180801, hour = 1 WHERE device_id = 11820004;
UPDATE smartem_raw.harvester_progress SET day = 20180801, hour = 1 WHERE device_id = 11820005;

-- 3. Delete all ASE-data from refined table
DELETE FROM smartem_refined.timeseries WHERE device_id/10000 = 1182;
