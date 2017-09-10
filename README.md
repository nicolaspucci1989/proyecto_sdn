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
``` bash
ryu-manager Hub.py
``` 
Ping entre h1 y h2
``` mininet
mininet> h1 ping -c5 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=84.5 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=13.9 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=14.2 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=14.4 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=15.6 ms

--- 10.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 13.922/28.544/84.521/27.994 ms
```
Prueba con iperf
``` mininet
mininet> iperf
*** Iperf: testing TCP bandwidth between h1 and h5 
*** Results: ['1.89 Mbits/sec', '2.08 Mbits/sec']
```
## Controlador como switch
iniciar controlador
``` bash
ryu-manager switch_simple.py
```
Ping entre h1 y h2
``` mininet
mininet> h1 ping -c5 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=59.1 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=1.10 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.229 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.192 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.190 ms

--- 10.0.0.2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4046ms
rtt min/avg/max/mdev = 0.190/12.164/59.103/23.472 ms
```
Prueba con iperf
``` mininet
mininet> iperf
*** Iperf: testing TCP bandwidth between h1 and h5 
*** Results: ['1.94 Gbits/sec', '1.94 Gbits/sec']
```
