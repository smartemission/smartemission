#!/bin/bash
#
# This prepares an empty Ubuntu system for running the SmartEmission Data Platform
# run this script onze as the admin user with full sudo rights: usually "ubuntu" or "vagrant"
# NB DO NOT RUN THIS AS root !!
#
# NB2 On Fiware lab VM: add "127.0.0.1 localhost hostname" to /etc/hosts

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y apt-transport-https ca-certificates  # usually already installed

# Add key
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

# Add to repo by putting this line in /etc/apt/sources.list.d/docker.list
sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >  ~/docker.list
sudo echo "" >> ~/docker.list

sudo mv ~/docker.list /etc/apt/sources.list.d/docker.list

sudo apt-get update

# check we get from right repo
# apt-cache policy docker-engine

# The linux-image-extra package allows you use the aufs storage driver.
# at popup keep locally installed config option
sudo apt-get install -y linux-image-extra-$(uname -r)

# If you are installing on Ubuntu 14.04 or 12.04, apparmor is required.
# You can install it using (usually already installed)
# sudo apt-get install -y apparmor

# install docker engine
sudo apt-get install -y docker-engine

# Start the docker daemon. Usually already running
sudo service docker start

# test
# sudo docker run hello-world

# Also Docker Compose
sudo apt-get install -y python-pip
sudo pip install docker-compose

# Utils like Emacs and Postgres client to connect to PG DB
sudo apt-get install -y emacs24-nox
sudo apt-get install -y postgresql-client-9.3

# The rest
# Github
sudo mkdir -p /opt/geonovum/smartem

sudo chown -R ${USER}:${USER} /opt/geonovum

cd /opt/geonovum/smartem

git clone https://github.com/Geonovum/smartemission.git git

echo "READY: now build and deploy components using Docker and Debian Packages"
