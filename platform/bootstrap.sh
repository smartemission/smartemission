#!/bin/bash
#
# This prepares an empty Ubuntu system for running the SmartEmission Data Platform
# run this script once as root.
# NB not required when your system already has Docker and docker-compose!!
#
#
# NB2 On Fiware lab VM: add "127.0.0.1 localhost hostname" to /etc/hosts
#
# Just van den Broecke - 2016-2018

# Bring system uptodate

# set time right adn configure timezone and locale
echo "Europe/Amsterdam" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

apt-get update
apt-get -y upgrade
apt-get install -y apt-transport-https ca-certificates  # usually already installed

# Add keys and extra repos
# /bin/rm /etc/apt/sources.list.d/docker.list /etc/apt/sources.list.d/pgdg.list

# Docker see https://docs.docker.com/engine/installation/linux/ubuntulinux/
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

# Add to repo by putting this line in /etc/apt/sources.list.d/docker.list
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >  /etc/apt/sources.list.d/docker.list

# Need 9.4 version of PG client, not in Ubuntu 14.4, so get from PG Repo
echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > /etc/apt/sources.list.d/pgdg.list
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

apt-get update

# check we get from right repo
# apt-cache policy docker-engine

# The linux-image-extra package allows you use the aufs storage driver.
# at popup keep locally installed config option
apt-get install -y linux-image-extra-$(uname -r)

# If you are installing on Ubuntu 14.04 or 12.04, apparmor is required.
# You can install it using (usually already installed)
# apt-get install -y apparmor

# install docker engine
apt-get install -y docker-engine

# Start the docker daemon. Usually already running
service docker start

# test
# docker run hello-world

# Utils like Emacs and Postgres client to connect to PG DB
# https://www.postgresql.org/download/linux/ubuntu/
# Need 9.4 version of PG client, not in Ubuntu 14.4, so get from PG Repo
apt-get install -y python-pip libyaml-dev libpython2.7-dev git emacs24-nox apache2-utils apt-show-versions sqlite3 postgresql-client-9.4

# Also Docker Compose
pip install pyyaml
pip install docker-compose

# Postfix: choose Local System
apt-get -y install postfix

# Smart Emission Github
mkdir -p /opt/geonovum/smartem

# chown -R ${USER}:${USER} /opt/geonovum

git clone https://github.com/Geonovum/smartemission.git /opt/geonovum/smartem/git

echo "READY: now run ./build.sh and ./install.sh to build and run SE Data Platform"
