ALTER TABLE v1.featureofinterest ADD COLUMN geojson jsonb;
ALTER TABLE v1.location ADD COLUMN geojson jsonb;

ALTER TABLE v1.observation DROP CONSTRAINT observation_pkey;
CREATE INDEX i_dsid_id
  ON v1.observation
  USING btree
  (stream_id, id);

