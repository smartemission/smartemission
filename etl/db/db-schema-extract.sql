 -- Database defs for extracted timeseries values of Smart Emission data

DROP SCHEMA IF EXISTS smartem_extracted CASCADE;
CREATE SCHEMA smartem_extracted;

-- ETL progress tabel, tracks last inserted timeseries (from raw sensor db) per device.
DROP TABLE IF EXISTS smartem_extracted.extractor_progress CASCADE;
CREATE TABLE smartem_extracted.extractor_progress (
  id serial,
  gid integer not null,
  PRIMARY KEY (id)
) WITHOUT OIDS;
