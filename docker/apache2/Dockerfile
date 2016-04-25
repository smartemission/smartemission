FROM ubuntu:14.04

MAINTAINER just@justobjects.nl

# Silence warnings
RUN export DEBIAN_FRONTEND=noninteractive TERM=linux && \
  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
  apt-get update && \
  apt-get -y upgrade

RUN apt-get install -y openssh-server apache2 supervisor libapache2-mod-wsgi python-flask python-psycopg2

RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor

RUN a2enmod headers
RUN a2enmod wsgi
RUN a2enmod proxy
RUN a2enmod proxy_ajp
RUN a2enmod proxy_http
RUN a2enmod cgi

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 22 80

CMD ["/usr/bin/supervisord"]
