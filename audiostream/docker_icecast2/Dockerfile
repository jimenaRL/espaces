FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y icecast2 ices2 && rm -rf /var/lib/apt/lists/*

ADD ./stream /stream
ADD . /app

RUN mkdir -p /var/log/ices/ && chmod 777 /var/log/ices/ && chmod +x /app/start.sh && chown -R icecast2.icecast /app

USER icecast2
WORKDIR /app

# docker build -t espaces_imaginaire:latest .
# docker run -it --rm  -p 8002:8000 --name icecast2 -v /etc/localtime:/etc/localtime:ro espaces_imaginaire:latest bash -c "icecast2 -c icecast.xml"
# docker run -it --rm --link icecast2:icecast2 espaces_imaginaire:latest bash -c "ices2 icecast-playlist.xml"

