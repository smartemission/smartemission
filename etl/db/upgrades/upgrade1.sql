-- 28 sept 2017 - needed for Smart City Living Lab

ALTER TABLE smartem_raw.timeseries  ALTER COLUMN device_id TYPE numeric;
ALTER TABLE smartem_raw.timeseries  ALTER COLUMN unique_id TYPE text;
ALTER TABLE smartem_raw.harvester_progress  ALTER COLUMN device_id TYPE numeric;
ALTER TABLE smartem_raw.harvester_progress  ALTER COLUMN unique_id TYPE text;

ALTER TABLE smartem_refined.refiner_progress  ALTER COLUMN device_id TYPE numeric;
ALTER TABLE smartem_refined.timeseries  ALTER COLUMN device_id TYPE numeric;

ALTER TABLE smartem_rt.last_device_output  ALTER COLUMN device_id TYPE numeric;
ALTER TABLE smartem_rt.last_device_output  ALTER COLUMN unique_id TYPE text;
