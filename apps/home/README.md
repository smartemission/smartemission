# Home Landing Page service

The `Home App` provides the landing page for the SE platform.

## Docker Image

The Docker image sources are hosted at: https://github.com/smartemission/docker-se-home
and the Image can be acquired from Docker Hub: https://hub.docker.com/r/smartemission/se-home

## Environment

The following environment vars need to be set, either via `docker-compose` or
Kubernetes.

|Environment Variable|Default
|---|---
|HERON_LOG_LEVEL|10 (debug)

## Architecture

The image contains a simple Flask webapp running in gunicorn WSGI server.
The app runs the Home static webpages. My be expanded in future.

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/
