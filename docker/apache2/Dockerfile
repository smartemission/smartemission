FROM ubuntu:14.04

MAINTAINER just@justobjects.nl

# Configure timezone and locale
RUN echo "Europe/Amsterdam" > /etc/timezone && \
	dpkg-reconfigure -f noninteractive tzdata

# Silence warnings   and set locales
# See also https://github.com/jacksoncage/phppgadmin-docker/blob/master/Dockerfile
RUN export LANGUAGE=en_US.UTF-8 && \
	export LANG=en_US.UTF-8 && \
	export LC_ALL=en_US.UTF-8 && \
	locale-gen en_US.UTF-8 && \
	export DEBIAN_FRONTEND=noninteractive TERM=linux && \
	echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
	dpkg-reconfigure locales && \
	apt-get update && \
	apt-get -y upgrade && \
    apt-get install -y openssh-server apache2 supervisor libapache2-mod-wsgi python-flask python-psycopg2 phppgadmin


RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor

RUN a2enmod headers
RUN a2enmod wsgi
RUN a2enmod proxy
RUN a2enmod proxy_ajp
RUN a2enmod proxy_http
RUN a2enmod cgi

# DB admin
COPY phppgadmin/phppgadmin.conf /etc/apache2/conf-available
COPY phppgadmin/config.inc.txt  /etc/phppgadmin/config.inc.php
RUN a2enconf phppgadmin

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY htpasswd /etc/apache2/.htpasswd

EXPOSE 22 80

CMD ["/usr/bin/supervisord"]
