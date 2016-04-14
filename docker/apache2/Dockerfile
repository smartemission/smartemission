FROM ubuntu:14.04

MAINTAINER just@justobjects.nl

# Silence warnings
RUN export DEBIAN_FRONTEND=noninteractive TERM=linux && \
  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
  apt-get update && \
  apt-get upgrade

RUN apt-get install -y openssh-server apache2 supervisor

RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 22 80

CMD ["/usr/bin/supervisord"]
