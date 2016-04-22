# passwd docker

export PGPASSWORD=docker

psql -h localhost -U docker gis -f db/db-schema-last.sql
