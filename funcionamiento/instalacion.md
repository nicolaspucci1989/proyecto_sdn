1. Adquirir y descomprimir tar
``` bash
wget http://openvswitch.org/releases/openvswitch-2.8.1.tar.gz
tar xvzf openvswitch-2.5.4.tar.gz
```
2. Instalar dependencias listadas en debian/config
``` bash
sudo apt-get install -y  graphviz \
                         autoconf \
                         automake \
                         bzip2 \
                         debhelper \
                         dh-autoreconf \
                         libssl-dev \
                         libtool \
                         openssl \
                         procps \
                         python-all \
                         python-qt4 \
                         python-twisted-conch \
                         python-zopeinterface
```
3. Comprobar dependencias con ```dpkg-checkbuilddeps```. No devuelve nada si no hubo errores.
4. Ejecutamos Serial build con unit tests para generar los .deb, 5 a 10 min.
``` bash
fakeroot debian/rules binary
```
5. Instalamos "openvswitch-switch" y "openvswitch-common"
``` bash
dpkg -i openvswitch-switch_2.5.4-1_i386.deb openvswitch-common_2.5.4-1_i386.deb
```
