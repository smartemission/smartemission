#!/bin/bash

# Sync GeoServer data/config to production

dir=/var/smartem/data/geoserver/
phost=root@data.smartemission.nl

rsync -e ssh -alzvx --delete ${dir} ${phost}:${dir}
