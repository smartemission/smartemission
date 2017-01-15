 -- Database defs for extracted timeseries values of Smart Emission data

DROP SCHEMA IF EXISTS smartem_calibrated CASCADE;
CREATE SCHEMA smartem_calibrated;

-- ETL calibration model table, stores all models
DROP TABLE IF EXISTS smartem_calibrated.calibration_models CASCADE;
CREATE TABLE smartem_calibrated.calibration_models (
  id serial,
  model bytea not null,
  predicts character varying (32) not null,
  score float,
  n int,
  invalid boolean not null default false,
  timestamp timestamp with time zone default current_timestamp,
  PRIMARY KEY (id)
) WITHOUT OIDS;
