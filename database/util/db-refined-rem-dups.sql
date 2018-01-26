select device_id, name, day, hour, count(*)
from "smartem_refined"."timeseries"
group by device_id, name, day, hour
HAVING count(*) > 1 order by device_id,day,hour

DELETE FROM "smartem_refined"."timeseries"
WHERE gid IN (SELECT gid
              FROM (SELECT gid,
                             ROW_NUMBER() OVER (partition BY device_id, name, day, hour ORDER BY gid) AS rnum
                     FROM "smartem_refined"."timeseries") t
              WHERE t.rnum > 1);
