 -- Database defs for extracted timeseries values of Smart Emission data

DROP SCHEMA IF EXISTS smartem_calibrated CASCADE;
CREATE SCHEMA smartem_calibrated;

-- ETL calibration model table, stores all models
DROP TABLE IF EXISTS smartem_calibrated.calibration_models CASCADE;
CREATE TABLE smartem_calibrated.calibration_models (
  id serial,
  parameters json,
  model bytea not null,
  input_order json,
  predicts character varying (32) not null,
  score float,
  n int,
  invalid boolean not null default false,
  timestamp timestamp with time zone default current_timestamp,
  PRIMARY KEY (id)
) WITHOUT OIDS;

DROP TABLE IF EXISTS smartem_calibrated.calibration_parameters CASCADE;
CREATE TABLE smartem_calibrated.calibration_parameters (
  id        SERIAL,
  predicts  CHARACTER VARYING (32) NOT NULL,
  parameter CHARACTER VARYING (32) NOT NULL,
  value     CHARACTER VARYING (32) NOT NULL,
  mean_test_score FLOAT,
  std_test_score  FLOAT,
  rank_test_score INT,
  mean_train_score FLOAT,
  std_train_score  FLOAT,
  mean_fit_time FLOAT,
  std_fit_time FLOAT,
  n         INT,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
  PRIMARY KEY (id)
) WITHOUT OIDS;

 DROP TABLE IF EXISTS smartem_calibrated.calibration_state CASCADE;
 CREATE TABLE smartem_calibrated.calibration_state (
   id SERIAL,
   process CHARACTER VARYING (32) NOT NULL,
   model_id INT,
   state JSON,
   timestamp TIMESTAMP with time zone default current_timestamp,
   PRIMARY KEY (id)
 ) WITHOUT OIDS;