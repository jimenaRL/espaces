## intall ices and its dependencies

# libxml2
wget ftp://xmlsoft.org/libxml2/libxml2-2.7.2.tar.gz
tar -zxf libxml2-2.7.2.tar.gz
cd libxml2-2.7.2
./configure
make
make install

# libogg
wget http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz
tar -zxf libogg-1.3.2.tar.gz
cd libogg-1.3.2
./configure
make
make install

# libvorbis
http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.gz
tar -zxf libvorbis-1.3.5.zip
cd libvorbis-1.3.5
./configure
make
make install

# libshout 2
wget http://downloads.xiph.org/releases/libshout/libshout-2.4.1.tar.gz
tar -zxf libshout-2.4.1.tar.gz
cd libshout-2.4.1
./configure
make
make install

# ices2
http://downloads.us.xiph.org/releases/ices/ices-2.0.2.tar.bz2
tar -zxf ices-2.0.2.tar.bz2
cd ices-0.4
./configure --with-lame
make
make install

