#!/bin/bash
#
# Build geoserver Docker image with options

sudo docker build --build-arg IMAGE_TIMEZONE="Europe/Amsterdam" --build-arg TOMCAT_EXTRAS=false --build-arg ORACLE_JDK=false  -t geonovum/geoserver .

# sudo docker build -t geonovum/geoserver .
