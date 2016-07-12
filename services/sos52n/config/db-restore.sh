# Databases
export PGUSER=docker
export PGPASSWORD=docker
export PGHOST=`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' postgis`
DB=gis

psql -h ${PGHOST} ${DB} < db-init.sql

# remove cache from SOS webapp
sudo docker exec -it sos52n  rm /usr/local/tomcat/webapps/sos52n/cache.tmp

pushd ..
./run.sh
popd
