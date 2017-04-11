# Smart Emission Services

Each directory below provides a ``run`` script and config to run
Docker containers for the SE services. ETL processing has its own directory.

## Architecture

The image below shows the Docker deployment architecture: how all containers
link together. NB it is also possible to run just a subset of these containers.
For example just InfluxDB and Grafana.

![docker arch](smartem-docker-s.jpg "SE Docker Deployment")

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/