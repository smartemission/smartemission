#!/bin/bash
#
# refresh smartemission website from GitHub
#
# run in cron every N mins- see sospilot crontab
#
cd /opt/geonovum/smartemission/git
./refresh-git.sh
