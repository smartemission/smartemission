#!/bin/bash

# Sync SOS data/config to production

dir=/var/smartem/data/sos52n/
phost=root@data.smartemission.nl

rsync -e ssh -alzvx --delete ${dir} ${phost}:${dir}
