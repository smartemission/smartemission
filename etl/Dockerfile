FROM geopython/stetl:latest

# Use the standard Stetl Docker Image with some additional packages
LABEL maintainer="Just van den Broecke <justb4@gmail.com>"

ENV ADD_PYTHON_DEB_PACKAGES="python-dev python-scipy python-seaborn python-matplotlib"  \
	ADD_PYTHON_PIP_PACKAGES="wheel Geohash influxdb scikit-learn==0.18"

RUN pip install --upgrade pip \
	&& apt-get update && apt-get --no-install-recommends install  -y \
	     ${ADD_PYTHON_DEB_PACKAGES} \
	    
	&& pip install ${ADD_PYTHON_PIP_PACKAGES} \
    && apt-get purge -y python-dev \
    && apt autoremove -y  \
    && rm -rf /var/lib/apt/lists/*


# Copy relevant files to work dir
ADD config /work/config
ADD smartem /work/smartem
ADD options/example.args /work/options/default.args
ADD scripts /work/scripts

WORKDIR /work

ENTRYPOINT ["/work/scripts/entry.sh"]
