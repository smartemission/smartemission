#!/bin/bash

# Runs the app with gunicorn

echo "START /entry.sh"

# Set timezone and time right in container.
# See: https://www.ivankrizsan.se/2015/10/31/time-in-docker-containers/ (Alpine)

# Set the timezone. Base image does not contain
# the setup-timezone script, so an alternate way is used.
if [ "$CONTAINER_TIMEZONE" = "" ];
then
	CONTAINER_TIMEZONE="Europe/Amsterdam"
else
	echo "Container timezone not modified"
fi

cp /usr/share/zoneinfo/${CONTAINER_TIMEZONE} /etc/localtime && \
echo "${CONTAINER_TIMEZONE}" >  /etc/timezone && \
echo "Container timezone set to: $CONTAINER_TIMEZONE date=`date`"


echo "Running Sosemu WSGI on ${CONTAINER_HOST}:${CONTAINER_PORT} with ${WSGI_WORKERS} workers"

cd /app

gunicorn --workers ${WSGI_WORKERS} \
		--worker-class=${WSGI_WORKER_CLASS} \
		--timeout ${WSGI_WORKER_TIMEOUT} \
		--name="Gunicorn_Heron" \
		--bind ${CONTAINER_HOST}:${CONTAINER_PORT} \
		index:app

echo "END /entry.sh"
