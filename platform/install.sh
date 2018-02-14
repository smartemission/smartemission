#!/bin/bash
#
# This installs all assets for SmartEmission Data Platform
# You must first have run ./bootstrap.sh and ./build.sh
#
# Just van den Broecke - 2016
#

script_dir=${0%/*}


mkdir -p /var/smartem/log/etl
chmod 777 /var/smartem/log/etl
mkdir -p /var/smartem/data
mkdir -p /var/smartem/backup

cp ${script_dir}/smartem.initd.sh /etc/init.d/smartem
chmod +x /etc/init.d/smartem

# Traditional TODO look into Upstart Way
update-rc.d smartem defaults

echo "READY: now start SE Data Platform using 'service smartem start'"
