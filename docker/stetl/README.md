# Stetl Docker

Docker image to run ETL tool Stetl. See www.stetl.org.

## Building

Use ./build.sh or

docker build -t smartemission/stetl:latest .

ARGs: optional --build-arg IMAGE_TIMEZONE="Europe/Amsterdam"

## Running

Mapping volumes can be handly to maintain all config and data outside the container. 
Note that full paths are required.

Example, running a basic Stetl example:

	cd test/1_copystd
	docker run -v `pwd`:`pwd` -w `pwd`  -t -i geonovum/stetl:latest -c etl.cfg   

Many Stetl configs require a connection to PostGIS. This can be effected with a linked container: ``--link postgis``, or
better using Docker networking.

See ../etl for examples.
