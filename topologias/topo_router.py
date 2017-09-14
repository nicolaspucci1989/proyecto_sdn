#!/usr/bin/python

"""
Este ejemplo convierte un nodo en un router usando forwarding de
IP disponible en Linux.

La topologia consiste en un router y tres subredes

    - 192.168.1.0/24 (r0-eth1, IP: 192.168.1.1)
    - 172.16.0.0/12 (r0-eth2, IP: 172.16.0.1)
    - 10.0.0.0/8 (r0-eth3, IP: 10.0.0.1)

Las dos primeras subredes consisten en dos host conectados
a un switch

    r0-eth1 - s1-eth1 - h1-eth0 (IP: 192.168.1.100)
    r0-eth1 - s1-eth2 - h2-eth0 (IP: 192.168.1.200)
    r0-eth2 - s2-eth3 - h3-eth0 (IP: 172.16.0.100)
    r0-eth2 - s2-eth4 - h4-eth0 (IP: 172.16.0.200)
    r0-eth3 - s3-eth5 - h5-eth0 (IP: 10.0.0.100)

El ejemplo se basa en las entradas de rutas que se crean
automaticamente para cada interface del router, de la
misma manera que los parametros del 'defaultRoute' para
la interface del host.

Es posible agregar rutas adicionales al router o host
ejecutando los comandos 'ip route' o 'route'.
"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class RouterSimple( Node ):
    "Nodo con IP forwarding habilitado."

    def config( self, **params ):
        super( RouterSimple, self).config( **params )
        # Habilitar IP forwarding
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( RouterSimple, self ).terminate()


class Topologia( Topo ):
    "El router conecta tres subredes"

    def build( self, **_opts ):

        defaultIP = '192.168.1.1/24'  # dir IP para r0-eth1
        router = self.addNode( 'r0', cls=RouterSimple, ip=defaultIP )

        s1, s2, s3, = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

        self.addLink( s1, router, intfName2='r0-eth1',
                      params2={ 'ip' : defaultIP } )
        self.addLink( s2, router, intfName2='r0-eth2',
                      params2={ 'ip' : '172.16.0.1/12' } )
        self.addLink( s3, router, intfName2='r0-eth3',
                      params2={ 'ip' : '10.0.0.1/8' } )

        h1 = self.addHost( 'h1', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1' )
        h2 = self.addHost( 'h2', ip='192.168.1.200/24',
                           defaultRoute='via 192.168.1.1' )
        h3 = self.addHost( 'h3', ip='172.16.0.100/12',
                           defaultRoute='via 172.16.0.1' )
        h4 = self.addHost( 'h4', ip='172.16.0.200/12',
                           defaultRoute='via 172.16.0.1' )
        h5 = self.addHost( 'h5', ip='10.0.0.100/8',
                           defaultRoute='via 10.0.0.1' )

        for h, s in [ (h1, s1), (h2, s1), (h3, s2), (h4, s2), (h5, s3) ]:
            self.addLink( h, s )


def run():
    "Test con router"
    topo = Topologia()
    net = Mininet( topo=topo )
    net.start()
    info( '*** Tabla de rutas:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
else:
    topos = { 'topologia': ( lambda: Topologia() ) }
