--
-- Upgrade GOST DB 0.5 --> 0.6
-- Just van den Broecke - april 17, 2018
--

-- NEW geojson shadow column for feature column
-- geojson column must be like {"type": "Point", "coordinates": [5.671321, 51.472583]}
ALTER TABLE v1.featureofinterest ADD COLUMN geojson jsonb;
UPDATE v1.featureofinterest SET geojson = concat('{"type": "Point", "coordinates": [' || ST_X(feature) || ', ' ||  ST_Y(feature) || ']}')::jsonb;


-- NEW geojson shadow column for feature column
ALTER TABLE v1.location ADD COLUMN geojson jsonb;
UPDATE v1.location SET geojson = concat('{"type": "Point", "coordinates": [' || ST_X(feature) || ', ' ||  ST_Y(feature) || ']}')::jsonb;


-- Optimizations for observation table
ALTER TABLE v1.observation DROP CONSTRAINT observation_pkey;
CREATE INDEX i_dsid_id
  ON v1.observation
  USING btree
  (stream_id, id);

