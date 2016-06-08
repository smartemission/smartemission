-- Database defs for raw timeseries (history) data for Smart Emission
DROP SCHEMA IF EXISTS smartem_raw CASCADE;
CREATE SCHEMA smartem_raw;

-- Raw device realtime output timeseries (history) table - data one2one from rawsensor api
DROP TABLE IF EXISTS smartem_raw.timeseries CASCADE;
CREATE TABLE smartem_raw.timeseries (
  gid serial,
  unique_id character varying (16),
  insert_time timestamp with time zone default current_timestamp,
  device_id integer,
  day integer,
  hour integer,
  data json,
  complete boolean default false,
  PRIMARY KEY (gid)
) WITHOUT OIDS;

DROP INDEX IF EXISTS timeseries_uid_idx;
CREATE UNIQUE INDEX timeseries_uid_idx ON smartem_raw.timeseries USING btree (unique_id) ;

-- VIEWS --
