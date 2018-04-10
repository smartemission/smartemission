# Waalkade Web Application

The `Waalkade` is a minimal web application for City of Nijmegen that shows the current values of
sensors and live video on Waalkade.

## Docker Image

The image is hosted at: https://github.com/smartemission/docker-se-waalkade
and acquired from Docker Hub: https://hub.docker.com/r/smartemission/se-waalkade

## Environment

At the moment no environment variables are required: the `Waalkade` will use the
locally running `sosemu` API.

## Architecture

The image contains a static HTML webapp running in an `nginx` webserver.
It uses Leaflet for mapping and Handlebars for client-side templating.

The app uses the `sosemu` API service which is called via JSONP from the browser.

## Links

* SE Platform doc: http://smartplatform.readthedocs.io/en/latest/
