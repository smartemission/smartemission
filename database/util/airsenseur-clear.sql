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


-- 1. Delete Harvested data from InfluxDB and
SELECT count(gid) FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;
DELETE FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;
SELECT count(gid) FROM smartem_raw.timeseries WHERE device_id/10000 = 1182;

-- 2. Reset Harvester State to start of calibration period (1.8.2018)
UPDATE smartem_raw.harvester_progress SET day = 180801, hour = 1 WHERE device_id/10000 = 1182;

-- 3. Delete all ASE-data from refined table
DELETE FROM smartem_refined.timeseries WHERE device_id/10000 = 1182;
