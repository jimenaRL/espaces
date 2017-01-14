FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq -y update && \
    apt-get -qq -y install icecast2 python-setuptools && \
    apt-get -qq -y install libshout3-dev && \
    apt-get -qq -y install libmp3lame0 libmp3lame-dev && \
    apt-get clean

RUN easy_install supervisor && \
    easy_install supervisor-stdout

RUN  apt-get update \
  && apt-get install -y wget \
  && apt-get -y install g++ \
  && apt-get -y install gcc \
  && apt-get -y install build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY ansible/roles/espaces/files/* /srv/workspace/install_scripts/

# Install ices
RUN /bin/bash /srv/workspace/install_scripts/ices_install.sh


CMD ["/start.sh"]
EXPOSE 8000
VOLUME ["/config", "/var/log/icecast2", "/etc/icecast2"]

ADD ./start.sh /start.sh
ADD ./etc /etc
ADD ./web /usr/share/icecast2/web
RUN chown -R icecast2 /etc/icecast2
