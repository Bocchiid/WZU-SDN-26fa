from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel


class SingleTopo3(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        for i in range(3):
            h = self.addHost('h%d' % (i + 1))
            self.addLink(h, s1)


if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleTopo3()
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    net.stop()