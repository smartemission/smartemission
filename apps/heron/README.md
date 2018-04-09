# Heron service

The `Heron Viewer`  provides a detailed viewer.

## Hosting

The Docker Image is hosted as: [smartemission/se-heron at DockerHub](https://hub.docker.com/r/smartemission/se-heron).

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
The app runs the Heron static webpages and some CGI/WSGI scripts.

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/
