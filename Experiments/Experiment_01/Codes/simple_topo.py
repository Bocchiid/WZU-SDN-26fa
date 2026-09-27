from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel


class SimpleTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        self.addLink(h1, s1)
        self.addLink(h2, s1)


if __name__ == '__main__':
    setLogLevel('info')
    topo = SimpleTopo()
    net = Mininet(topo=topo)
    net.start()

    h1, h2 = net.get('h1'), net.get('h2')
    print("h1 IP:", h1.IP())
    print("h2 IP:", h2.IP())
    net.pingAll()

    CLI(net)
    net.stop()