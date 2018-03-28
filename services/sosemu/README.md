# sosemu service

The `sosemu` service provides a minimal (52North) SOS REST API
with the goal of providing **last values** for each station.

This service was developed initially within the SE project to
support the SmartApp, in absence of SOS at that time.

This service will be deprecated, to be replaced by SensorThings API via `GOST`.

## Environment

The following environment vars need to be set, either via `docker-compose` or
Kubernetes.

|Environment variable|
|---|
|SOSEMU_DB_HOST|
|SOSEMU_DB_PORT|
|SOSEMU_DB_NAME|
|SOSEMU_DB_SCHEMA|
|SOSEMU_DB_USER|
|SOSEMU_DB_PASSWORD|

## Architecture

The image contains a simple Flask webapp running in gunicorn WSGI server.
The app directly connects to the SE Database tables for last values.

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/
