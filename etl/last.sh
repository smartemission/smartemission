#!/bin/bash
#
# ETL for reading last values from Smart Emission CityGIS Raw Sensor API
#

sudo docker run --link postgis2:postgis2 -v `pwd`:`pwd` -w `pwd`  -t -i geonovum/stetl -c last.cfg -a options/docker.args