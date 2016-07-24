#!/bin/bash

dir=/var/smartem/data/sos52n/
# thost=root@test.smartemission.nl
phost=root@data.smartemission.nl

rsync --dry-run -e ssh -alzvx --delete ${dir} ${phost}:${dir}