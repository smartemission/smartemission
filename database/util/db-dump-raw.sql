
-- see http://dba.stackexchange.com/questions/90482/export-postgres-table-as-json
-- see http://stackoverflow.com/questions/24006291/postgresql-return-result-set-as-json-array
COPY (SELECT to_json(t) FROM ( select * from smartem_raw.timeseries where device_id = 26 and day > 20160627 limit 2) t) to '/var/smartem/backup/raw.json';
