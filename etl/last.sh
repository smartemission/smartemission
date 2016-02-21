#!/bin/bash
#
# ETL for reading last values from Smart Emission CityGIS Raw Sensor API
#

# Usually required in order to have Python find your package
export PYTHONPATH=${PWD}/python:${PYTHONPATH}

stetl_cmd=stetl

# debugging
# stetl_cmd=../../../../stetl/git/stetl/main.py

# Host-specific options (args) file to be substitued in .cfg
options_file=options/`hostname`.args

${stetl_cmd} -c last.cfg -a ${options_file}

