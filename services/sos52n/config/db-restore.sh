# Databases
export PGUSER=docker
export PGPASSWORD=docker
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`
DB=gis

psql -h ${PGHOST} ${DB} < db-init.sql
