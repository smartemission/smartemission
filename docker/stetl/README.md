# Stetl Docker

Docker image to run Stetl www.stetl.org commands.

## Building

docker build -t geonovum/stetl .

## Running

Mapping volumes can be handly to maintain all config and data outside the container. 
Note that full paths are required.

	cd test/1_copystd
	docker run -v `pwd`:`pwd` -w `pwd`  -t -i geonovum/stetl -c etl.cfg   

Many Stetl configs require a connection to PostGIS. This can be effected with a linked container: ``--link postgis``, or
better using Docker networking.

See ../etl for examples.
