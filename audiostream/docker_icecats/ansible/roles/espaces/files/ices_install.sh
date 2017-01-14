wget http://downloads.us.xiph.org/releases/ices/ices-0.4.tar.gz
tar -zxf ices-0.4.tar.gz
cd ices-0.4
./configure --with-lame
make
make install