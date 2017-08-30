#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller
from os import environ

RYUDIR = environ[ 'HOME' ] + '/Documents/UNSAM/proyecto/sdn/notas'

class RYU( Controller ):
    def start(self):
        self.ryu =  '%s/DumbSwitch.py' % RYUDIR
        self.cmd('ryu-manager %s &' % self.ryu )

    def stop( self ):
        self.cmd( 'pkill ryu-manager' )


class SingleSwitchTopo(Topo):

    def build(self):
        hosts = []
        switch = []

        for h in range(5):
            hosts.append(self.addHost('h%s' % (h + 1),
                mac='00:00:00:00:00:0%s' % ( h + 1 )))

        for s in range(3):
            switch.append(self.addSwitch('s%s' % (s + 1)))

        self.addLink(hosts[0], switch[0])
        self.addLink(hosts[1], switch[0])
        self.addLink(hosts[2], switch[1])
        self.addLink(hosts[4], switch[2])
        self.addLink(hosts[3], switch[1])

        self.addLink(switch[0], switch[1])
        self.addLink(switch[1], switch[2])


if __name__ == '__main__':
    topo = SingleSwitchTopo()
    # Asignar topologia y puerto para acceder con dpctl,
    # si no usar ovs-ofctl
    # ej, s1 dpctl dump-talbes tcp:127.0.0.1:6634
    # Puerto por defecto 6633
    setLogLevel( 'info' )
    net = Mininet(topo, listenPort=6634, controller=RYU)
    net.start()
    CLI(net)
    net.stop()

else: # Si no es main, es argumento de mn
    topos = {'mytopo': ( lambda: SingleSwitchTopo() )}
