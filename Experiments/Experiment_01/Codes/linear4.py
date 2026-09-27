from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel


class LinearTopo4(Topo):
    def build(self):
        switches = []
        for i in range(4):
            s = self.addSwitch('s%d' % (i + 1))
            switches.append(s)
            h = self.addHost('h%d' % (i + 1))
            self.addLink(h, s)
        
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1])


if __name__ == '__main__':
    setLogLevel('info')
    topo = LinearTopo4()
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    net.stop()