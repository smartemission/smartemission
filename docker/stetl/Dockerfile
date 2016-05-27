FROM ubuntu:14.04
# FROM python:2.7

MAINTAINER just@justobjects.nl

# Configure timezone and locale
RUN echo "Europe/Amsterdam" > /etc/timezone && \
	dpkg-reconfigure -f noninteractive tzdata

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
# ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng
RUN export DEBIAN_FRONTEND=noninteractive TERM=linux && \
  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN apt-add-repository ppa:ubuntugis/ubuntugis-unstable
RUN apt-get -y update

#-------------Application Specific Stuff ----------------------------------------------------

#     python-imaging \
#      python-yaml \
#    libjpeg-dev \
#    zlib1g-dev \
#    libfreetype6-dev \
#    python-virtualenv

RUN apt-get install -y \
	git \
    libproj0 \
    libgeos-dev \
    python-lxml \
    python-gdal \
    libgdal-dev \
    build-essential \
    python-dev \
    python-setuptools

# ADD start.sh /start.sh
# RUN chmod 0755 /start.sh
RUN git clone https://github.com/justb4/stetl /opt/stetl

RUN cd /opt/stetl; python setup.py install

ENTRYPOINT ["/usr/local/bin/stetl"]
