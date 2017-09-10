#!/usr/bin/python


'''
comando para mn con topo custom con controlador mininet
sudo mn --custom topo2.py --topo mytopo --switch ovsk --controller remote
iniciar controlador ryu
ryu-manager L2Switch
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller
from os import environ

L2SWITCH = environ[ 'HOME' ] + '/Documents/UNSAM/proyecto/sdn/notas/L2Switch.py'
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
        # Listas para hosts y switches
        self.hsts = []
        self.swchs = []

        # Crear los hosts y asignarles una MAC
        for h in range(5):
            self.hsts.append(self.addHost('h%s' % (h + 1)))

        # Crear switches
        for s in range(3):
            self.swchs.append(self.addSwitch('s%s' % (s + 1),
                                            mac='00:00:00:00:55:0%s' % ( s + 1)))

        # Conectamos los hosts a los switches
        self.addLink(self.hsts[0], self.swchs[0])
        self.addLink(self.hsts[1], self.swchs[0])
        self.addLink(self.hsts[2], self.swchs[1])
        self.addLink(self.hsts[3], self.swchs[1])
        self.addLink(self.hsts[4], self.swchs[2])

        # Conectamos los switches entre si
        self.addLink(self.swchs[0], self.swchs[1])
        self.addLink(self.swchs[1], self.swchs[2])


def testSencillo():
    topo = TopoFETH()
    setLogLevel( 'info' )
    net = Mininet(topo, listenPort=6634, controller=RYU)
    net.start()
    #h1 = net.hosts[ 0 ]
    #h2 = net.hosts[ 1 ]
    s1 = net.get( 's1' )
    #print h1.cmd( 'ping -c3', h2.IP() )
    s1.cmd('dpctl add-flow tcp:127.0.0.1:6634 in_port=1,actions=output:2' )
    s1.cmd('dpctl add-flow tcp:127.0.0.1:6634 in_port=2,actions=output:1' )
    CLI(net)
    #print s1.cmd( 'dpctl dump-flows tcp:127.0.0.1:6634' )
    #print h1.cmd( 'ping -c3', h2.IP() )
    net.stop()

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
