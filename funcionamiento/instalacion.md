1. Instalar dependencias listadas en debian/config
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
2. Comprobar dependencias con ```dpkg-checkbuilddeps```. No devuelve nada si no hubo errores.
3. Ejecutamos Serial build con unit tests para generar los .deb, 5 a 10 min.
``` bash
fakeroot debian/rules binary
```
4. Instalamos "openvswitch-switch" y "openvswitch-common"
``` bash
dpkg -i openvswitch-switch_2.5.4-1_i386.deb openvswitch-common_2.5.4-1_i386.deb
```
