Hypervisors necesitan la posibilidad de puentear tráfico entre VMs y el mundo exterior. En Hypervisors basados en Linux esto significaba usar el switch ya incorporado (Linux bridge) el cual es rápido y confiable. Entonces por qué usar Open vSwitch.

OVS apunta a los desplieges de servidores multi-virtualización, un panorama para el cual Linux bridge no es lo más adecuado. Estos entornos estan caracterizados por extremos altamente dinámicos, mantenimiento de abstracciones lógicas, y a veces la integración o descarga a hardware especializado en switching.

Open vSwitch es un switch OpenFlow que tipicamente es usado con hypervisors con el fin de interconectar maquinas virtuales dentro de un host y maquinas virtuales dentro de distintos hosts a lo largo de varias redes. También es usado en algunos tipos de hardware dedicado al switching. Puede ser una parate crítica en una solución SDN.

OVS soporta las siguentes características:
* VLAN taggin y 802.1q trunking.
* Standar spanning tree protocol (802.1D).
* LACP.
* Port mirroring (SPAN/RSPAN).
* Flow export.
* Tunneling (GRE, VXLAN, IPSEC).
* Control QoS.

``` bash
ovs-vsctl add-br mybridge
ovs-vsctl show
ifconfig mybridge up
```
para eliminar: ```ovs-vsctl del-br mybridge```
``` bash
ovs-vsctl add-port mybridge eth0
ovs-vsctl show
ping google.com
```
ping falla
```

```
