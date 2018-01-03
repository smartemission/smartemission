ALTER TABLE smartem_raw.timeseries  ADD COLUMN IF NOT EXISTS
  device_type character varying not null default 'jose';
ALTER TABLE smartem_raw.timeseries  ADD COLUMN IF NOT EXISTS
  device_version character varying not null default '1';
