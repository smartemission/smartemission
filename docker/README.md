# Docker

Below are the generic Docker image recipes. These generic docker images is used by the ETL and services. 
Via volume mappings
dynamic and configuration data is kept on the host. This makes the Docker images highly reusable.
A complete open geostack system can be setup in minutes!

## Getting Started

To make a standard Ubuntu (14.4+) system ready for using
Docker, run the ../platform/bootstrap.sh script as a user with sudo-root rights (not root itself!).
Then call build.sh on each of the Docker images in the subdirs. Or build all within
../platform calling ./build.sh there.

## Usage in ETL and Services

See the ../services and ../etl "run" shell-scripts for the use of these Docker images.

For example the Stetl Docker image is used in various ETL shell scripts.

## Examples

See run.sh scripts under ../services/<service>

Run postgis

sudo docker run --name "postgis" -p 5432:5432 -d IMAGE=geonovum/postgis:9.4-2.1
psql -h localhost -U docker  -l

Remove images
sudo docker rm -v $(sudo docker ps -a -q -f status=exited)
