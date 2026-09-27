from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel


class TreeTopo(Topo):
    def build(self, depth=2, fanout=2):
        root = self.addSwitch('s1')
        self._addTree(root, depth, fanout, level=1, counter=[1])

    def _addTree(self, parent, depth, fanout, level, counter):
        if level >= depth:
            for _ in range(fanout):
                counter[0] += 1
                h = self.addHost('h%d' % counter[0])
                self.addLink(parent, h)
            return
        for _ in range(fanout):
            counter[0] += 1
            s = self.addSwitch('s%d' % counter[0])
            self.addLink(parent, s)
            self._addTree(s, depth, fanout, level + 1, counter)


if __name__ == '__main__':
    setLogLevel('info')
    topo = TreeTopo(depth=2, fanout=2)
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    net.stop()