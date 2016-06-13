Place 52NOrth SOS  config files here.

These files are copied permanently into the Docker image
as these are not possible to map via symlinks from host:

- datasource.properties
- logback.xml

The third config file that the SOS needs is WEB-INF/configuration.db.
A default version is provided here. However, to be able to maintain
this file over reruns of the Docker image a Docker volume mount should be
done within the service invokation. See services/sos52n.
