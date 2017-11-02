 -- Database defs for metadata Smart Emission data

DROP SCHEMA IF EXISTS smartem_meta CASCADE;
CREATE SCHEMA smartem_meta;

-- ETL progress tabel, tracks last inserted timeseries (from raw sensor db) per device.
DROP TABLE IF EXISTS smartem_meta.project CASCADE;
CREATE TABLE smartem_meta.project (
  id integer not null,
  sub_id integer not null,
  full_id integer not null,
  name text not null,
  sub_name text not null,
  tag text not null,
  device text not null,
  description text not null,
  last_update timestamp with time zone default current_timestamp,
  PRIMARY KEY (full_id)
) WITHOUT OIDS;

INSERT INTO smartem_meta.project(id, sub_id, full_id, name, sub_name, tag, device, description)
      VALUES (0, 0, 0, 'Smart Emission Nijmegen', 'Smart Emission Nijmegen', 'senij_0000_jose1', 'Intemo Josene v1', 'Original SE project');

INSERT INTO smartem_meta.project(id, sub_id, full_id, name, sub_name, tag, device, description)
      VALUES (20, 1, 2001, 'Smart City Living Lab', 'Zoetermeer', 'scliv_2001_jose1', 'Intemo Josene v1', 'SC LL for Zoetermeer');

--  Sub projecten  Smart City Living Lab
-- Leidschendam;Helmond;Veldhoven;Breda;Dordrecht;Zoetermeer;Rijswijk

-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('scliv_2260_jose1', 'Smart City Living Lab', 'Leidschendam', 'Intemo Josene v1', 2260);
--
-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('scliv_5700_jose1', 'Smart City Living Lab', 'Helmond', 'Intemo Josene v1', 5700);
--
-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('scliv_5500_jose1', 'Smart City Living Lab', 'Veldhoven', 'Intemo Josene v1', 5500);
--
-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('scliv_4800_jose1', 'Smart City Living Lab', 'Breda', 'Intemo Josene v1', 4800);
--
-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('scliv_3300_jose1', 'Smart City Living Lab', 'Dordrecht', 'Intemo Josene v1', 3300);
--
-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('scliv_2700_jose1', 'Smart City Living Lab', 'Zoetermeer', 'Intemo Josene v1', 2700);
--
-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('scliv_2280_jose1', 'Smart City Living Lab', 'Rijswijk', 'Intemo Josene v1', 2280);
--
-- INSERT INTO smartem_meta.tagdef(tag, project, area, device, id_prefix)
--       VALUES ('eujrc_1181_as1', 'EU JRC', 'Netherlands', 'AirSensEUR', 1181);
