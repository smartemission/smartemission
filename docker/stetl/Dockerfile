FROM geopython/stetl:latest

# Use the standard Stetl Docker Image with some additional packages
LABEL maintainer "Just van den Broecke <justb4@gmail.com>"

ENV ADD_PYTHON_DEB_PACKAGES="python-dev python-scipy python-seaborn python-matplotlib"
ENV ADD_PYTHON_PIP_PACKAGES="wheel Geohash influxdb scikit-learn==0.18"

RUN pip install --upgrade pip \
	&& apt-get update && apt-get --no-install-recommends install  -y \
	     ${ADD_PYTHON_DEB_PACKAGES} \
	    
	&& pip install ${ADD_PYTHON_PIP_PACKAGES} \
    && apt-get purge -y python-dev \
    && apt autoremove -y  \
    && rm -rf /var/lib/apt/lists/*

## OBSOLETE OLD STUFF - kept for ref a bit
## FROM python:2.7  would be preferred but trickier
## TODO: use a more lightweight Linux distro than Ubuntu
#
#MAINTAINER just@justobjects.nl
#
## Configure timezone and locale
#ARG IMAGE_TIMEZONE="Europe/Amsterdam"
## set time right adn configure timezone and locale
#RUN echo "$IMAGE_TIMEZONE" > /etc/timezone && \
#	dpkg-reconfigure -f noninteractive tzdata
#
## Optional: Use local cached debs from host (saves your bandwidth!)
## Change ip below to that of your apt-cacher-ng host
## Or comment this line out if you do not with to use caching
## ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng
#
#RUN export DEBIAN_FRONTEND=noninteractive TERM=linux && \
#  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
#
#RUN apt-get update && \
#	apt-get install -y software-properties-common
#
## Use UbuntuGIS for latest GDAL, Proj.4, GEOS etc
#RUN apt-add-repository ppa:ubuntugis/ubuntugis-unstable
#RUN apt-get update && \
#	apt-get install -y git \
#    libgeos-dev \
#    python-lxml \
#    python-gdal \
#    libgdal-dev \
#    build-essential \
#    python-dev \
#    python-setuptools \
#    python-pip
#
## For Python extra packages
#RUN sudo pip install --upgrade pip
#
## Timezone support in Python
#RUN pip install pytz
#
## Requests support in Python
#RUN pip install requests
#
## Geohash https://en.wikipedia.org/wiki/Geohash support in Python
#RUN pip install geohash
#
## Development version of scikit-learn
#RUN pip install Cython numpy pandas scipy scikit-learn==0.18
#
## Influxdb python client
#RUN pip install influxdb
#
## Pretty visualization support in python
#RUN pip install seaborn matplotlib
#
## Get latest Stetl from git
#RUN git clone https://github.com/geopython/stetl /opt/stetl
#
## Use Stetl installer
#RUN cd /opt/stetl; python setup.py install

# Allow docker run
# ENTRYPOINT ["/usr/local/bin/stetl"]
