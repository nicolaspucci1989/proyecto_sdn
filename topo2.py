#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

class SingleSwitchTopo(Topo):

    def build(self):
        hosts = []
        switch = []

        for h in range(5):
            hosts.append(self.addHost('h%s' % (h + 1)))

        for s in range(3):
            switch.append(self.addSwitch('s%s' % (s + 1)))

        self.addLink(hosts[0], switch[0])
        self.addLink(hosts[1], switch[0])
        self.addLink(hosts[2], switch[1])
        self.addLink(hosts[3], switch[1])
        self.addLink(hosts[4], switch[2])

        self.addLink(switch[0], switch[1])
        self.addLink(switch[1], switch[2])


topo = SingleSwitchTopo()
#Asignar topologia y puerto para acceder con dpctl, si no usar ovs-ofctl
net = Mininet(topo, listenPort=6634)
net.start()
CLI(net)
net.stop()
