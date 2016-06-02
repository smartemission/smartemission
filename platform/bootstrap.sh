#!/bin/bash
#
# This prepares an empty Ubuntu system for running the SmartEmission Data Platform
# run this script once as root.
#
# NB2 On Fiware lab VM: add "127.0.0.1 localhost hostname" to /etc/hosts
#
# Just van den Broecke - 2016

# Bring system uptodate

# set time right adn configure timezone and locale
echo "Europe/Amsterdam" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y apt-transport-https ca-certificates  # usually already installed

# Add keys and extra repos
# /bin/rm /etc/apt/sources.list.d/docker.list /etc/apt/sources.list.d/pgdg.list

# Docker see https://docs.docker.com/engine/installation/linux/ubuntulinux/
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

# Add to repo by putting this line in /etc/apt/sources.list.d/docker.list
sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >  /etc/apt/sources.list.d/docker.list

# Need 9.4 version of PG client, not in Ubuntu 14.4, so get from PG Repo
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > /etc/apt/sources.list.d/pgdg.list
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

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

# Utils like Emacs and Postgres client to connect to PG DB
# https://www.postgresql.org/download/linux/ubuntu/
# Need 9.4 version of PG client, not in Ubuntu 14.4, so get from PG Repo
sudo apt-get install -y  python-pip libyaml-dev libpython2.7-dev git emacs24-nox apache2-utils apt-show-versions postgresql-client-9.4

# Also Docker Compose
sudo pip install pyyaml
sudo pip install docker-compose

sudo mkdir -p /var/smartem/log/etl
sudo chmod 777 /var/smartem/log/etl
sudo mkdir -p /var/smartem/data
sudo mkdir -p /var/smartem/backup

# Postfix: choose Local System
sudo apt-get install postfix

# view tail -f /va
# The rest
# Github
sudo mkdir -p /opt/geonovum/smartem

# sudo chown -R ${USER}:${USER} /opt/geonovum

cd /opt/geonovum/smartem

git clone https://github.com/Geonovum/smartemission.git git

echo "READY: now run ./build.sh and ./install.sh to build and run SE Data Platform"
