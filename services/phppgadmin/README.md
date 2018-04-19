# PHPPGAdmin

Provides PostgreSQL management WebUI using PHPPGAdmin Image from Dockage.

No SE specific Docker Image is required. 


## Hosting

The Docker Image is hosted by the wonderful [Dockage organisation](https://hub.docker.com/u/dockage/)
as: [dockage/phppgadmin](https://hub.docker.com/r/dockage/phppgadmin/).  The Dockage GitHub Org is at
https://github.com/dockage.

## Environment

There are many env vars [defined in the documentation](https://github.com/dockage/phppgadmin). Most have sensible defaults.
Only SE-relevant env vars  are listed below. 
 
These need to be set via `docker-compose` or Kubernetes.

|Environment variable|
|---|
|PHP_PG_ADMIN_SERVER_HOST|
|PHP_PG_ADMIN_SERVER_PORT|

## Architecture

The official [dockage/phppgadmin](https://hub.docker.com/r/dockage/phppgadmin/) Image is directly used.
This image follows an interesting reusable Docker design as it is derived from this chain of ancestor images:

* [dockage/alpine-nginx-php-fpm](https://hub.docker.com/r/dockage/alpine-php-fpm/) - Docker PHP-FPM image built on Alpine Linux
* [dockage/alpine-confd/](https://hub.docker.com/r/dockage/alpine-confd/) - Docker confd, built on Alpine Linux. confd is a lightweight configuration management tool.
* [dockage/alpine-openrc/](https://hub.docker.com/r/dockage/alpine-openrc/) - [OpenRC](https://en.wikipedia.org/wiki/OpenRC) as a process supervision on Alpine Linux
* [dockage/alpine/](https://hub.docker.com/r/dockage/alpine/) - Alpine image that forms the base for Dockage's docker images
* [alpine/](https://hub.docker.com/_/alpine/) - A minimal Docker image based on Alpine Linux (only 5 MB in size!)

## Links

* Dockage GitHub: https://github.com/dockage
* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/

