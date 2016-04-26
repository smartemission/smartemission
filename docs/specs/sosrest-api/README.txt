This contains the relevant services for the (emulated) implementation 52North SOS REST API
within the Smart Emision project.

Only two relevant services are implemented from the full 52N spec:
http://sensorweb.demo.52north.org/sensorwebclient-webapp-stable/api-doc/index.html

The API location for the (emulated) Smart Emission SOS RESt API:
http://api.smartemission.nl/sosemu/

The .json files under this directory
show example output from the various 52North SOS REST API services:
IRCELine, RIVM, Geonovum SOSPilot, Smart Emission.

API calls for simple SOS REST API for Smart Emission:

# base Url
See http://api.smartemission.nl/sosemu

# Get stations
http://api.smartemission.nl/sosemu/api/v1/stations

# Get timeseries (for last values) for station 23
http://api.smartemission.nl/sosemu/api/v1/timeseries?station=23&expanded=true

# JSONP Support via callback= parameter
http://api.smartemission.nl/sosemu/api/v1/stations?format=json&callback=mycallback

# Example with Leaflet (uses JSONP)
http://rawgit.com/Geonovum/smartemission/master/specs/sosrest-api/examples/leaflet.html

# code for examples under
https://github.com/Geonovum/smartemission/tree/master/specs/sosrest-api/examples

