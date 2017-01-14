FROM ubuntu:trusty

COPY ansible/roles/espaces/files/* /srv/workspace/install_scripts/

# Install tools
RUN /bin/bash /srv/workspace/install_scripts/tools_install.sh

# Install icecast and ices
RUN /bin/bash /srv/workspace/install_scripts/icecast2_install.sh
RUN /bin/bash /srv/workspace/install_scripts/ices_install.sh
#RUN /bin/bash /srv/workspace/install_scripts/shout-python_install.sh

#CMD ["/start.sh"]
EXPOSE 8000
VOLUME ["/config", "/var/log/icecast2", "/etc/icecast2"]

ADD ./start.sh /start.sh
ADD ./etc /etc
ADD ./web /usr/share/icecast2/web
RUN chown -R icecast2 /etc/icecast2
