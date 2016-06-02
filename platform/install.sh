#!/bin/bash
#
# This installs all assets for SmartEmission Data Platform
# You must first have run ./bootstrap.sh and ./build.sh
#
# Just van den Broecke - 2016
#

script_dir=${0%/*}

sudo cp ${script_dir}/smartem.initd.sh /etc/init.d/smartem
sudo chmod +x /etc/init.d/smartem

# Traditional TODO look into Upstart Way
sudo update-rc.d smartem defaults

echo "READY: now start SE Data Platform using 'service smartem start'"
