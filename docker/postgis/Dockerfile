FROM kartoza/postgis:9.4-2.1

# TODO for now kartoza/postgis:9.4-2.1 fulfills all needs
# Configure timezone and locale
RUN echo "Europe/Amsterdam" > /etc/timezone && \
	dpkg-reconfigure -f noninteractive tzdata
