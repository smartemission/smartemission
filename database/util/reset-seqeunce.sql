-- noinspection SqlNoDataSourceInspectionForFile
CREATE OR REPLACE FUNCTION "reset_sequence" (tablename text, columnname text, sequence_name text) RETURNS "pg_catalog"."void" AS

    $body$
      DECLARE
      BEGIN

      EXECUTE 'SELECT setval( ''' || sequence_name  || ''', ' || '(SELECT MAX(' || columnname || ') FROM ' || tablename || ')' || '+1)';



      END;

    $body$  LANGUAGE 'plpgsql';


-- select timeseries || '_' || gid || '_seq', reset_sequence(timeseries, gid, timeseries || '_' || gid || '_seq') from information_schema.columns where column_default like 'nextval%';

-- this works http://stackoverflow.com/questions/4678110/how-to-reset-sequence-in-postgres-and-fill-id-column-with-new-data
UPDATE timeseries SET gid=1000000+ nextval('timeseries_gid_seq');
ALTER SEQUENCE timeseries_gid_seq RESTART WITH 1;
UPDATE timeseries SET gid=nextval('timeseries_gid_seq');
