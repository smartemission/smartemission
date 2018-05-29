# PGAdmin4

Provides PostgreSQL management WebUI using the public PGAdmin4 Image 
from .

No SE-specific Docker Image is required. 


## Hosting

The Docker Image is hosted on DockerHub at 
[dpage/pgadmin4](https://hub.docker.com/r/dpage/pgadmin4/).  
The related GitHub is athttps://github.com/postgres/pgadmin4.

## Environment

There are few env vars as listed below. 
 
These need to be set via `docker-compose` or Kubernetes.

|Environment variable|
|---|
|PGADMIN_DEFAULT_EMAIL|
|PGADMIN_DEFAULT_PASSWORD|

## Architecture

The relatively new PGAdmin4 app is a complete rewrite from the well-known PGAdminIII
desktop app. The app is written as a (Flask/ReactJS) webapp and can be deployed as
either a platform-specific desktop or a web-application. The Docker-version uses 
the webapp.

## Links

* GitHub: https://github.com/postgres/pgadmin4
* PGAdmin4 Project: https://redmine.postgresql.org/projects/pgadmin4
* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/

