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

-- ETL progress tabel, houdt bij voor laatst ingelezen timeseries is per device .
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
CREATE OR REPLACE FUNCTION refiner_progress_update() RETURNS TRIGGER AS $refiner_progress_update$
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
    FOR EACH ROW EXECUTE PROCEDURE refiner_progress_update();

-- VIEWS --
-- TBD
