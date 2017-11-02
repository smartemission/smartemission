#!/bin/bash
#
# Build Stetl Docker image

# Optional timezone

# sudo docker build -t --build-arg IMAGE_TIMEZONE="Europe/Amsterdam" geonovum/stetl:latest .

sudo docker build -t smartemission/stetl:latest .

