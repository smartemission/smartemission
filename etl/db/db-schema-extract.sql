 -- Database defs for extracted timeseries values of Smart Emission data

DROP SCHEMA IF EXISTS smartem_extracted CASCADE;
CREATE SCHEMA smartem_extracted;

-- ETL progress tabel, tracks last inserted timeseries (from raw sensor db) per device.
DROP TABLE IF EXISTS smartem_extracted.refiner_progress CASCADE;
CREATE TABLE smartem_extracted.refiner_progress (
  gid serial,
  insert_time timestamp with time zone default current_timestamp,
  gid_raw integer not null,
  device_id integer not null,
  day integer not null,
  hour integer not null,
  PRIMARY KEY (gid)
) WITHOUT OIDS;
