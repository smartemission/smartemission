# passwd docker

export PGPASSWORD=docker

# Use local connection, we do not expose PG to outside world
psql -h `docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis` -U docker -W gis -f db/db-schema-last.sql

# psql -h localhost -U docker gis -f db/db-schema-last.sql
