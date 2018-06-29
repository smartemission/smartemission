#!/bin/bash
#
# This prepares an empty Ubuntu system for running the SmartEmission Data Platform
# run this script once as root.
# NB not required when your system already has Docker and docker-compose!!
# Best to not run entire script but copy the lines to shell
#
# Only for Ubuntu 16.04 !!!
# 
# Just van den Broecke - 2016-2018

# AZURE VM first mount disk!
# Mount disk Azure
# https://docs.microsoft.com/en-us/azure/virtual-machines/linux/add-disk
# dmesg - get device e.g. /dev/sdc
# fdisk /dev/sdc
# n (new partition, p, defaults etc )
# /dev/sdc1        2048 1048575999 1048573952  500G 83 Linux
# mkfs -t ext4 /dev/sdc1
# mkdir /var/smartem
#
# get Block ID
# sudo -i blkid
# bijv /dev/sdc1: UUID="b67a6a57-393b-4c44-868c-6acd4eabcff5" TYPE="ext4" PARTUUID="1c7a5211-01"
# dan in /etc/fstab
# UUID=b67a6a57-393b-4c44-868c-6acd4eabcff5   /var/smartem   ext4   defaults,nofail   1   2
# zou automounted moeten zijn.

# Bring system uptodate

# set time right adn configure timezone and locale
#echo "Europe/Amsterdam" > /etc/timezone
#dpkg-reconfigure -f noninteractive tzdata

timedatectl set-timezone Europe/Amsterdam

apt-get update
apt-get -y upgrade

# Docker CE
# see https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add to repo 
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-cache policy docker-ce
apt-get install -y docker-ce

# Check Docker daemon
systemctl status docker


# Utils like Emacs and Postgres client to connect to PG DB
# https://www.postgresql.org/download/linux/ubuntu/
# Need 9.4 version of PG client, not in Ubuntu 14.4, so get from PG Repo
# apt-get install -y python-pip libyaml-dev libpython2.7-dev git emacs24-nox apache2-utils apt-show-versions sqlite3 postgresql-client-9.4
apt-get install -y emacs24-nox
apt-get install -y git python-pip libyaml-dev libpython2.7-dev postgresql-client-common postgresql-client
apt-get install -y apt-show-versions sqlite3

# apache2-utils??

# Also Docker Compose
pip install pyyaml
pip install docker-compose

# Postfix: choose Local System
# apt-get -y install postfix

# Smart Emission Github
mkdir -p /opt/geonovum/smartem

# chown -R ${USER}:${USER} /opt/geonovum

git clone https://github.com/smartemission/smartemission.git /opt/geonovum/smartem/git

# now put in .args files at right places
# /opt/geonovum/smartem/git/etl/options/<host>.args
# /opt/geonovum/smartem/git/services/influxdb/influxdb.env
# /opt/geonovum/smartem/git/services/influxdb-dc/influxdb.env
#
# Create all database schemas
# ./init-databases.sh
# Populate Calibrated from backup: gis-smartem_calibrated_171003.dmp

# Install system service "smartem"
# ./install.sh

echo "READY: now do 'service smartem run' to start SE Data Platform"

# OLD STUFF
# Need 9.4 version of PG client, not in Ubuntu 14.4, so get from PG Repo
# echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > /etc/apt/sources.list.d/pgdg.list
# curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# apt-get update

# check we get from right repo
# apt-cache policy docker-engine

# The linux-image-extra package allows you use the aufs storage driver.
# at popup keep locally installed config option
# apt-get install -y linux-image-extra-$(uname -r)

# If you are installing on Ubuntu 14.04 or 12.04, apparmor is required.
# You can install it using (usually already installed)
# apt-get install -y apparmor

# install docker engine
# apt-get install -y docker-engine

# Start the docker daemon. Usually already running
# service docker start

# test
# docker run hello-world
