apt-get -qq -y update
apt-get -qq -y install icecast2 python-setuptools
apt-get -qq -y install libshout3-dev
apt-get -qq -y install libmp3lame0 libmp3lame-dev
apt-get clean

easy_install supervisor
easy_install supervisor-stdout

