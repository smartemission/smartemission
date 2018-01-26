-- Database defs for extracted timeseries values of Smart Emission data

DROP SCHEMA IF EXISTS smartem_harvest_rivm CASCADE;
CREATE SCHEMA smartem_harvest_rivm;

-- ETL progress tabel, tracks last inserted timeseries (from raw sensor db) per device.
DROP TABLE IF EXISTS smartem_harvest_rivm.progress CASCADE;
CREATE TABLE smartem_harvest_rivm.progress (
  id          SERIAL,
  timestamp   BIGINT                NOT NULL,
  name        CHARACTER VARYING(128) NOT NULL,
  last_update TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
  PRIMARY KEY (id)
) WITHOUT OIDS;

-- TRIGGER to update checkpointing by storing last day/hour for each device
-- Thus the Harvester always knows where to start from when running
CREATE OR REPLACE FUNCTION smartem_harvest_rivm.progress_update(new_timestamp BIGINT,
  new_name character)
  RETURNS BOOLEAN AS $result$
BEGIN
  --
  -- Set the progress for the device id to the last day+hour harvested
  -- make use of the special variable TG_OP to work out the operation.
  --

  DELETE FROM smartem_harvest_rivm.progress
  WHERE name = new_name;

  INSERT INTO smartem_harvest_rivm.progress (timestamp, name)
  VALUES (new_timestamp, new_name);

  RETURN NULL; -- result is ignored since this is an AFTER trigger
END;
$result$ LANGUAGE plpgsql;
