Place 52NOrth SOS  config files here.

These files are copied permanently into the Docker image
as these are not possible to map via symlinks from host:

- datasource.properties
- logback.xml

The third config file that the SOS needs is WEB-INF/configuration.db.
A default version is provided here. However, to be able to maintain
this file over reruns of the Docker image a Docker volume mount should be
done within the service invokation. See services/sos52n.

Note: the password is set here to the default: CHANGE THIS AFTER INSTALL
via the Admin itnerface (Credentials).

NB you may want to change the admin password back to the default:
https://wiki.52north.org/bin/view/SensorWeb/SosFAQ#How_to_apply_Tomcat_HTTP_basic_a

INSERT OR REPLACE INTO administrator_user(id, username, password) VALUES
   (1, 'admin', '$2a$10$vbp9aXCDMP/fXwEsqe/1.eon44mMdUyC4ub2JfOrkPfaer5ciLOly');