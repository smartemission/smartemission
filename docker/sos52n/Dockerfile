#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Inspired by : https://github.com/kartoza/docker-sos52n/blob/master/Dockerfile
# Enhancements to be added there !!
# FROM tomcat:8.0

# 52NorthSOS 4.3+ requires JRE7 !
FROM tomcat:8.0.35-jre7

MAINTAINER Just van den Broecke<just@justobjects.nl>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
# ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get -y update

ARG IMAGE_TIMEZONE="Europe/Amsterdam"
# set time right adn configure timezone and locale
RUN echo "$IMAGE_TIMEZONE" > /etc/timezone && \
	dpkg-reconfigure -f noninteractive tzdata

#-------------Application Specific Stuff ----------------------------------------------------
#  .zip file: http://52north.org/downloads/send/3-sos/484-52n-sensorweb-sos-bundle-4-3-7
ENV SOS_VERSION 4.3.7
ENV SOS_DL_URL http://52north.org/downloads/send/3-sos/484-52n-sensorweb-sos-bundle-4-3-7
ENV TC_DEPLOY_DIR $CATALINA_HOME/webapps
ENV SOS_CONFIG_DIR  /opt/sosconfig
ENV SOS_DEPLOY_DIR  $TC_DEPLOY_DIR/sos52n

# Prepare dirs
RUN mkdir -p $TC_DEPLOY_DIR
RUN mkdir -p $SOS_CONFIG_DIR

# Unset Java related ENVs since they may change with Oracle JDK
ENV JAVA_VERSION=
ENV JAVA_DEBIAN_VERSION=

# Set JAVA_HOME to /usr/lib/jvm/default-java and link it to OpenJDK installation
RUN ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/lib/jvm/default-java
ENV JAVA_HOME /usr/lib/jvm/default-java

# ADD resources /tmp/resources
ADD resources /tmp/resources

# If a matching Oracle JDK tar.gz exists in /tmp/resources, move it to /var/cache/oracle-jdk7-installer
# where oracle-java7-installer will detect it
RUN if ls /tmp/resources/*jdk-*-linux-x64.tar.gz > /dev/null 2>&1; then \
      mkdir /var/cache/oracle-jdk7-installer && \
      mv /tmp/resources/*jdk-*-linux-x64.tar.gz /var/cache/oracle-jdk7-installer/; \
    fi;

# Install Oracle JDK (and uninstall OpenJDK JRE) if the build-arg ORACLE_JDK = true or an Oracle tar.gz
# was found in /tmp/resources
ARG ORACLE_JDK=false
RUN if ls /var/cache/oracle-jdk7-installer/*jdk-*-linux-x64.tar.gz > /dev/null 2>&1 || [ "$ORACLE_JDK" = true ]; then \
       apt-get autoremove --purge -y openjdk-7-jre-headless && \
       echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true \
         | debconf-set-selections && \
       echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu precise main" \
         > /etc/apt/sources.list.d/webupd8team-java.list && \
       apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886 && \
       apt-get update && \
       apt-get install -y oracle-java7-installer oracle-java7-set-default && \
       ln -s --force /usr/lib/jvm/java-7-oracle /usr/lib/jvm/default-java && \
       rm -rf /var/lib/apt/lists/* && \
       rm -rf /var/cache/oracle-jdk7-installer; \
       if [ -f /tmp/resources/jce_policy.zip ]; then \
         unzip -j /tmp/resources/jce_policy.zip -d /tmp/jce_policy && \
         mv /tmp/jce_policy/*.jar $JAVA_HOME/jre/lib/security/; \
       fi; \
    fi;

# A little logic that will fetch the sos52n war zip file if it
# is not available locally in the resources dir
RUN if [ ! -f /tmp/resources/sos52n.zip ]; then \
      wget -c $SOS_DL_URL -O /tmp/resources/sos52n.zip; \
    fi;

# unzips in sos52n/52n-sensorweb-sos-bundle-$SOS_VERSION/bin/target/52n-sos-webapp##4.3.6.war
# hence mv to a Linux-friendly filename
RUN unzip /tmp/resources/sos52n.zip -d /tmp/resources/sos52n  \
    && unzip '/tmp/resources/sos52n/52n-sensorweb-sos-bundle-4.3.6/bin/target/52n-sos-webapp##4.3.6.war' -d $SOS_DEPLOY_DIR

# Move all relevant settings files to a separate dir and provide symlinks
# These can then be provided externally via a volume mount from the host to the container
# Hence these files can be preserved outside the docker image/container, surviving restarts.
# NB this cuerrently only works for configuration.db, the others need to be copied!
RUN cp -f /tmp/resources/config/configuration.db $SOS_CONFIG_DIR \
    && ln -s $SOS_CONFIG_DIR/configuration.db $SOS_DEPLOY_DIR

# Hard-copy the config files that we are not able to symlink
RUN if ls /tmp/resources/config/datasource.properties > /dev/null 2>&1; then \
      cp -f /tmp/resources/config/datasource.properties $SOS_DEPLOY_DIR/WEB-INF; \
    fi; \
    if ls /tmp/resources/config/logback.xml > /dev/null 2>&1; then \
      cp -f /tmp/resources/config/logback.xml $SOS_DEPLOY_DIR/WEB-INF/classes; \
    fi;

# Overlay files and directories in resources/overlays if they exist
RUN rm /tmp/resources/overlays/README.txt && \
    if ls /tmp/resources/overlays/* > /dev/null 2>&1; then \
      cp -rf /tmp/resources/overlays/* /; \
    fi;

# Optionally remove Tomcat manager, docs, and examples
ARG TOMCAT_EXTRAS=true
RUN if [ "$TOMCAT_EXTRAS" = false ]; then \
    rm -rf $TC_DEPLOY_DIR/ROOT && \
    rm -rf $TC_DEPLOY_DIR/docs && \
    rm -rf $TC_DEPLOY_DIR/examples && \
    rm -rf $TC_DEPLOY_DIR/host-manager && \
    rm -rf $TC_DEPLOY_DIR/manager; \
  fi;

# Delete resources after installation
RUN rm -rf /tmp/resources
