# Heron service

The `Heron Viewer` provides a detailed viewer for current and history sensor values.

## Hosting

The Docker Image is hosted as: [smartemission/se-heron at DockerHub](https://hub.docker.com/r/smartemission/se-heron).

## Environment

The following environment vars need to be set, either via `docker-compose` or
Kubernetes.

|Environment Variable|Default
|---|---
|HERON_PROXY_REFERERS|localhost,smartemission.nl,geonovum.nl,heron-mc.org
|HERON_PROXY_HOSTS|map5.nl,knmi.nl,nationaalgeoregister.nl,nlextract.nl,rivm.nl,smartemission.nl
|HERON_LOG_LEVEL|20

## Architecture

The image contains a simple Flask webapp running in gunicorn WSGI server.
The app runs the Heron static webpages and some CGI/WSGI scripts.

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/
