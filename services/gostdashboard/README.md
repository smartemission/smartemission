# SensorThings API - GOST Dashboard

This service configures and runs 
the  [GOST Dashboard V2](https://github.com/gost/dashboard-v2) server using 
the [GOST Dashboard V2 Docker Image](https://store.docker.com/community/images/geodan/gost-dashboard-v2).

The Dashboard used to be part of the GOST Server but since v0.4 it has 
been moved to a separate repo and Docker Image. First as `gost/dashboard` (Angular),
now as `gost/dashboard-v2` (developed with Web Components and Polymer)

## Running

Use the command `./run.sh` and `./stop.sh` or
                           
```
export HOSTNAME
docker-compose up

```

## Links

* GOST Server - https://github.com/gost/server
* GOST DB - https://github.com/gost/gost-db
* GOST Dashboard - https://github.com/gost/dashboard-v2
