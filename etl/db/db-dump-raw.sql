
-- see http://dba.stackexchange.com/questions/90482/export-postgres-table-as-json
-- see http://stackoverflow.com/questions/24006291/postgresql-return-result-set-as-json-array
COPY (SELECT to_json(t) FROM ( select * from smartem_raw.timeseries limit 10) t) to '/var/smartem/backup/raw.json';
