Instalar dependencias listadas en debian/config
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

Comprobar dependencias con ```dpkg-checkbuilddeps```. Si no hay errores no devuelve nada.
Ejecutamos Serial build con unit tests.
``` bash
fakeroot debian/rules binary
```
Instalamos "openvswitch-switch" y "openvswitch-common"
``` bash
dpkg -i openvswitch-switch_2.5.4-1_i386.deb openvswitch-common_2.5.4-1_i386.deb
```
