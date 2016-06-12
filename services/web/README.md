# Web service

This service configures and runs the generic Docker (Apache2) web services.
This is the front-end for the entire SE Data Platform. 

## Running

Use the command ./run.sh

## Services

Several service endpoints are available:

/sosemu the SOS emulator, temporary SOS untill full SOS available
/geoserver  proxy to backend GeoServer for WMS, WFS
/sos proxy to backed SOS (TBS)

## Apps

Several SE apps are hosted:

/smartapp the SmartApp
/heron  the Heron Viewer

## Configuring

The website is configured via the Apache2 site-config file config/sites-enabled/000-default.conf

To use admin features a file "htpasswd" should be created in the directory config/admin. 
Create there by using the command:

htpasswd -c htpasswd <username>

It will ask for a password twice. Obviously the file "htpasswd" should not be in GitHub
but created locally!

phppgadmin can be used to inspect the database. Its configuration is in config/phppgadmin/config.inc.php

## Admin

A simple admin subsite is available via the /adm URL. This is secured using basic authentication.
See above how to generate the HTTP password. NB no HTTPS is used yest, so never use 
the admin site at e.g. public WIFIs!




