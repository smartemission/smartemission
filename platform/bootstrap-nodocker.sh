#!/bin/bash
#
# This prepares a Ubuntu system for running the SmartEmission Data Platform
# Run this script once as root.
#
# Assumes Docker(-compose) and Git already installed!
#
# Just van den Broecke - 2018

timedatectl set-timezone Europe/Amsterdam

apt-get update
apt-get -y upgrade

apt-get install -y apache2-utils apt-show-versions postgresql-client

# Smart Emission Github
mkdir -p /opt/geonovum/smartem

# chown -R ${USER}:${USER} /opt/geonovum

git clone https://github.com/smartemission/smartemission.git /opt/geonovum/smartem/git

echo "READY: now run ./build.sh and ./install.sh to build and run SE Data Platform"
