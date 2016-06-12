Place any config files here that are not possible to map via symlinks from host:

Currently:

- datasource.properties
- logback.xml

The third config file that the SOS needs is WEB-INF/configuration.db. Here symlinks
do work, plus this file is changing more often. We supply this file within the services/sos52n.
