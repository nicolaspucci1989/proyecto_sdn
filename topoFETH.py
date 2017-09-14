#!/usr/bin/python


'''
comando para mn con topo custom con controlador mininet
sudo mn --custom topo2.py --topo mytopo --switch ovsk --controller remote
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import Controller
from mininet.cli import CLI
from os import environ


L2SWITCH = environ[ 'HOME' ] + '/Documents/UNSAM/proyecto/sdn/notas/controladores/switch_simple.py'
RYUEJEMPLOS = environ[ 'HOME' ] + '/ryu/ryu/app/simple_switch.py'

class RYU( Controller ):
    def start(self):
        # Asignamos el controlador
        self.ryu =  '%s' % L2SWITCH
        # Asignamos el comando necesario para correr el controlador
        self.cmd('ryu-manager %s &' % self.ryu )

    def stop( self ):
        self.cmd( 'pkill ryu-manager' )


class TopoFETH(Topo):
    def build(self):
        # Crear los hosts y asignarles una MAC
        h1, h2, h3, h4, h5 = [ self.addHost( h ) for h in ( 'h1', 'h2', 'h3', 'h4', 'h5' ) ]

        # Crear switches
        s1, s2, s3 = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

        # Conectamos los hosts a los switches
        for h, s in [ (h1, s1), (h2, s1), (h3, s2), (h4, s2), (h5, s3)]:
            self.addLink( h, s )

        # Conectamos los switches entre si
        for x, y in [ (s1, s2), (s2, s3) ]:
            self.addLink( x, y )


if __name__ == '__main__':
    topo = TopoFETH()
    ## Asignar topologia y puerto para acceder con dpctl,
    ## si no usar ovs-ofctl
    ## ej, s1 dpctl dump-talbes tcp:127.0.0.1:6634
    ## Puerto por defecto 6633
    setLogLevel( 'info' )
    net = Mininet(topo, listenPort=6634, controller=RYU)
    net.start()
    CLI(net)
    net.stop()
else: # Si no es main, es argumento de mn
    topos = {'topologia': ( lambda: TopoFETH() )}
