# Databases
export PGUSER=docker
export PGPASSWORD=docker
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.Networks.se_back.IPAddress }}' postgis`
DB=gis

pg_dump -h ${PGHOST} --if-exists --schema=sos52n1 --clean ${DB}  > db-init.sql
