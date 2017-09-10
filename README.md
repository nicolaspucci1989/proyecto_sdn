## Trabajos a realizar
1. Que el grupo conozca el software y los rudimentos del uso de SDN
2. Armar maqueta con una red virtual para poder realizar diferentes pruebas. (mininet)
   * 3 switches en cascada (FETH)
   * 1 controlador
   * 1 servidor
   * 1 PC
3. Correr ejercicios, realizar pruebas y obtener resultados
   * Prueba de conectividad entre los nodos
      * Ping
      * Trafico
      * Falla
      * Redundancia
   * Implementacion de SDN
     * Uso sin configurar
     * Configurar Switches como HUBS
     * Configurar Switches como Switches
     * Configurar Switches como Routers
     * Medir performace de cada configuracion
---
## Software Necesario
1. Sistema operativo Linux.
2. Mininet.
  Instalacion:
  ``` bash
  git clone git://github.com/mininet/mininet
  mininet/util/install.sh -a
  ```
  Test funcionalidad basica:
  ``` bash
  sudo mn --test pingall
  ```
3. Ryu.
 Instalacion:
 ``` bash
 git clone git://github.com/osrg/ryu.git
 cd ryu; python ./setup.py install
 ```
---
## Controlador pasivo
Iniciar topologia:
``` bash
sudo mn --custom topo2.py --topo mytopo --switch ovsk --controller remote
```
Iniciar controlador
``` bash
ryu-manager controlador_pasivo.py
```
El controlador recibe paquetes de los switches pero no realiza ninguna acción.

## Controlador como hub
Iniciar controlador
```
ryu-manager Hub.py
```
Ping entre h1 y h2
```
mininet> h1 ping -c5 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=19.6 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=15.3 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=16.5 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=11.7 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=10.9 ms

--- 10.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 10.900/14.824/19.616/3.198 ms
```
