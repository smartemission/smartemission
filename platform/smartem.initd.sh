#!/bin/sh
#
# init.d script with LSB support for entire Smart Emission Data Platform.
#
# Copyright (c) 2016 Just van den Broecke for Geonovum - <just@justobjects.nl>
#
# This is free software; you may redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2,
# or (at your option) any later version.
#
# This is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License with
# the Debian operating system, in /usr/share/common-licenses/GPL;  if
# not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307 USA
#
### BEGIN INIT INFO
# Provides:          smartem
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remote_fs
# Should-Start:      $named
# Should-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Open Geospatial Stack for Smart Emission Data: starts most services via Docker(-compose)
# Description:       Manages run cycle for a set of Docker containers together providing the Smart Emission Data Platform.
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

NAME=smartem
DESC="Smart Emission Data Platform"
SMARTEM_HOME=/opt/geonovum/smartem/git/platform

. /lib/lsb/init-functions

# set -e

status_platform() {
	docker ps
	crontab -l
    return 0
}

start_platform() {
	${SMARTEM_HOME}/start.sh
	status_platform
    return 0
}

stop_platform() {
	${SMARTEM_HOME}/stop.sh
	status_platform
    return 0
}


case "$1" in
  start)
	log_daemon_msg "Starting $DESC" "$NAME"
	start_platform
	;;

  stop)
	log_daemon_msg "Stopping $DESC" "$NAME"
	stop_platform
	;;

  restart)
	log_daemon_msg "Restarting $DESC" "$NAME"
	$0 stop
	$0 start
	;;

  status)
	log_daemon_msg "Checking status of $DESC" "$NAME"
	status_platform
	;;

  reinit)
	log_warning_msg "Reinit of $NAME"
	stop_platform
	$0 start
	;;

  *)
	N=/etc/init.d/$NAME
	echo "Usage: $N {start|stop|restart|reinit|status}" >&2
	exit 1
	;;
esac

exit 0
