# SmartApp Web Application

The `SmartApp` is a minimal web application that shows the current values of
SE sensor stations.

## Environment

The following environment vars need to be set, either via `docker-compose` or
Kubernetes.

|Environment variable|
|---|
|SMARTAPP_DATA_URL default '/sosemu/api/v1'|

## Architecture

The image contains a static HTML webapp running in an `nginx` webserver.
It uses Leaflet for mapping and Handlebars for client-side templating.

The app uses the `sosemu` API service which is called via JSONP from the browser.

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/
