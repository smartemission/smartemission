FROM kartoza/postgis:9.4-2.1

# TODO for now kartoza/postgis:9.4-2.1 fulfills all needs
ARG IMAGE_TIMEZONE="Europe/Amsterdam"
# set time right adn configure timezone and locale
RUN echo "$IMAGE_TIMEZONE" > /etc/timezone && \
	dpkg-reconfigure -f noninteractive tzdata
