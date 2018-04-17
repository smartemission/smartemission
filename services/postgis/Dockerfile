FROM kartoza/postgis:9.4-2.1

# SE specific additions
COPY config/*.conf /etc/postgresql/9.4/main/

# TODO for now kartoza/postgis:9.4-2.1 fulfills all needs
ARG IMAGE_TIMEZONE="Europe/Amsterdam"
# set time right adn configure timezone and locale
RUN echo "$IMAGE_TIMEZONE" > /etc/timezone && \
	dpkg-reconfigure -f noninteractive tzdata
