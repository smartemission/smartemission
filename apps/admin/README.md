# Admin Landing Page service

The `Admin App` provides admin pages for the SE platform.

## Docker Image

The Docker image sources are hosted at: https://github.com/smartemission/docker-se-admin
and the Image can be acquired from Docker Hub: https://hub.docker.com/r/smartemission/se-admin

## Environment

The following environment vars need to be set, either via `docker-compose` or
Kubernetes.

|Environment Variable|Default
|---|---
|ADMIN_LOG_LEVEL|10 (debug)

## Architecture

The image contains a simple Flask webapp running in gunicorn WSGI server.
The app runs the Admin static webpages. My be expanded in future.

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/
