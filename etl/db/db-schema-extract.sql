 -- Database defs for extracted timeseries values of Smart Emission data

DROP SCHEMA IF EXISTS smartem_extracted CASCADE;
CREATE SCHEMA smartem_extracted;

-- ETL progress tabel, tracks last inserted timeseries (from raw sensor db) per device.
DROP TABLE IF EXISTS smartem_extracted.extractor_progress CASCADE;
CREATE TABLE smartem_extracted.extractor_progress (
  id serial,
  last_gid integer not null,
  name character varying (32) not null,
  last_update timestamp with time zone default current_timestamp,
  PRIMARY KEY (id)
) WITHOUT OIDS;

INSERT INTO smartem_extracted.extractor_progress(last_gid, name) VALUES (0, 'all');