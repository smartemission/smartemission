# Docker

Below the Docker image recipes.

## Shorthands

Run postgis

sudo docker run --name "postgis" -p 5432:5432 -d -t kartoza/postgis:9.4-2.1
psql -h localhost -U docker  -l

Remove images
sudo docker rm -v $(sudo docker ps -a -q -f status=exited)
