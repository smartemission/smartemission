#!/bin/bash
#
# Build 52North SOS Docker image with options

sudo docker build --no-cache --build-arg IMAGE_TIMEZONE="Europe/Amsterdam" --build-arg TOMCAT_EXTRAS=false --build-arg ORACLE_JDK=false  -t geonovum/sos52n:4.3.7 .
