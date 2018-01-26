-- 
-- Update feature geometry from refined table stations VIEW last location
-- An Enormous Hack: but there is no way to achieve this via the SOS Protocol!
-- See issue https://github.com/Geonovum/smartemission/issues/72


UPDATE sos52n1.featureofinterest as fi
SET
  geom  = stations.point
FROM   smartem_refined.stations as stations
WHERE  fi.identifier = 'fid-' || cast (stations.device_id as character varying(255))
