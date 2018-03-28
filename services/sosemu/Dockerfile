FROM python:2.7.13-alpine

LABEL maintainer="Just van den Broecke <justb4@gmail.com>"

# These are default values,
# Override when running container via docker(-compose)

# General ENV settings
ENV LC_ALL="en_US.UTF-8" \
	LANG="en_US.UTF-8" \
	LANGUAGE="en_US.UTF-8" \
	# WSGI server settings, assumed is gunicorn  \
	CONTAINER_HOST=0.0.0.0 \
	CONTAINER_PORT=80 \
	WSGI_WORKERS=4 \
	WSGI_WORKER_TIMEOUT=6000 \
	WSGI_WORKER_CLASS='eventlet' \
	\
	# DB-specific: provide at runtime via compose or Kube \
	SOSEMU_DB_NAME=db \
	SOSEMU_DB_HOST=pg \
	SOSEMU_DB_PORT=5432 \
	SOSEMU_DB_SCHEMA=sche  \
	SOSEMU_DB_USER=usr \
	SOSEMU_DB_PASSWORD=pwd


RUN apk add --no-cache --virtual .build-deps gcc build-base linux-headers postgresql-dev \
    && apk add --no-cache bash postgresql-client tzdata openntpd \
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/* \
    && pip install psycopg2 eventlet gunicorn flask

# Add runscript and app to root dir
COPY entry.sh /
ADD app /app

# Install and Remove build-related packages for smaller image size
RUN chmod a+x /*.sh && apk del .build-deps

EXPOSE ${CONTAINER_PORT}

ENTRYPOINT /entry.sh
