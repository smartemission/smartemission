# Apache2 Docker

Inspired by https://docs.docker.com/engine/admin/using_supervisord/ and
https://github.com/jacksoncage/phppgadmin-docker/blob/master/Dockerfile (PHP and locales).

Docker image runs both Apache2 and SSH daemons.


## Building

sudo docker build -t geonovum/apache2 .

## Running

     sudo docker run -p 2222:22 -p 80:80 -t -i  geonovum/apache2

This runs the image and exposes ports 2222 and 8081 mapping these to the standard
ports 22 and 80 within the container.

Mapping volumes can be handly to maintain all config and data outside the container. 
Note that full paths are required.

     sudo docker run -d -p 2222:22 -p 80:80 -v `pwd`/log:/var/log/apache2 -t -i  geonovum/apache2
  
