# Docker

Below the generic Docker image recipes. To make a standard UBuntu system ready for using
Docker, run the bootstrap.sh script as a user with sudo-root rights (not root itself!).

Each of the generic docker images is used by the ETL and services. Via volume mappings
dynamic and configuration data is kept on the host.

## Shorthands

Run postgis

sudo docker run --name "postgis" -p 5432:5432 -d -t kartoza/postgis:9.4-2.1
psql -h localhost -U docker  -l

Remove images
sudo docker rm -v $(sudo docker ps -a -q -f status=exited)
