# Apache2 Docker

Inspired by https://docs.docker.com/engine/admin/using_supervisord/.

Docker image runs both Apache2 and SSH daemons.

## Building

docker build -t geonovum/apache2 .

## Running

     docker run -p 2222:22 -p 8081:80 -t -i  geonovum/apache2

This runs the image and exposes ports 2222 and 8081 mappoing these to the standard
ports 22 and 80 within the container.

NB on Mac OSX via docker machine the actual IP adress is not 127.0.0.1 but e.g. 192.168.99.100
since Docker runs within VirtualBox VM.

Mapping volumes can be handly to maintain all config and data outside the container. 
Note that full paths are required.

     docker run -p 2222:22 -p 8081:80 -v `pwd`/log:/var/log/apache2 -t -i  geonovum/apache2
  
