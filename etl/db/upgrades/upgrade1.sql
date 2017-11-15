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
