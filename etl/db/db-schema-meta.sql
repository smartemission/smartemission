 -- Database defs for metadata Smart Emission data

DROP SCHEMA IF EXISTS smartem_meta CASCADE;
CREATE SCHEMA smartem_meta;

-- ETL progress tabel, tracks last inserted timeseries (from raw sensor db) per device.
DROP TABLE IF EXISTS smartem_meta.tagdef CASCADE;
CREATE TABLE smartem_meta.tagdef (
  id serial,
  tag text not null,
  project text not null,
  area text not null,
  device text not null,
  id_prefix integer not null,
  last_update timestamp with time zone default current_timestamp,
  PRIMARY KEY (id)
) WITHOUT OIDS;

-- maxint is 2147 483647
INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('senij_0000_jose1', 'Smart Emission Nijmegen', 'Netherlands', 'Intemo Josene v1', 0000);

--  Codes Smart City Living Lab
-- Leidschendam;Helmond;Veldhoven;Breda;Dordrecht;Zoetermeer;Rijswijk
-- 2260-001;5700-001;5500-001;4800-001;3300-001;2700-001;2280-001
-- 2260-002;5700-002;5500-002;4800-002;3300-002;2700-002;2280-002
-- 2260-003;5700-003;5500-003;4800-003;3300-003;2700-003;2280-003
-- 2260-004;5700-004;5500-004;4800-004;3300-004;2700-004;2280-004
-- 2260-005;5700-005;5500-005;4800-005;3300-005;2700-005;2280-005
-- 2260-006;5700-006;5500-006;4800-006;3300-006;2700-006;2280-006
-- 2260-007;5700-007;5500-007;4800-007;3300-007;2700-007;2280-007
-- 2260-008;5700-008;5500-008;4800-008;3300-008;2700-008;2280-008
-- 2260-009;5700-009;5500-009;4800-009;3300-009;2700-009;2280-009
-- 2260-010;5700-010;5500-010;4800-010;3300-010;2700-010;2280-010

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('scliv_2260_jose1', 'Smart City Living Lab', 'Leidschendam', 'Intemo Josene v1', 2260);

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('scliv_5700_jose1', 'Smart City Living Lab', 'Helmond', 'Intemo Josene v1', 5700);

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('scliv_5500_jose1', 'Smart City Living Lab', 'Veldhoven', 'Intemo Josene v1', 5500);

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('scliv_4800_jose1', 'Smart City Living Lab', 'Breda', 'Intemo Josene v1', 4800);

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('scliv_3300_jose1', 'Smart City Living Lab', 'Dordrecht', 'Intemo Josene v1', 3300);

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('scliv_2700_jose1', 'Smart City Living Lab', 'Zoetermeer', 'Intemo Josene v1', 2700);

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('scliv_2280_jose1', 'Smart City Living Lab', 'Rijswijk', 'Intemo Josene v1', 2280);

INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
      VALUES ('eujrc_1181_as1', 'EU JRC', 'Netherlands', 'AirSensEUR', 1181);
