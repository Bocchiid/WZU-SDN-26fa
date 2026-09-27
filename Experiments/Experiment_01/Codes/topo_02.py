from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

net = Mininet(link=TCLink)
c0 = net.addController()
h0 = net.addHost('h0')
s0 = net.addSwitch('s0')
h1 = net.addHost('h1')

net.addLink(s0, h0, bw=20, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
net.addLink(h1, s0)

h0.setIP('192.168.1.1', 24)
h1.setIP('192.168.1.2', 24)

net.start()
net.pingAll()
net.iperf((h0, h1))
CLI(net)
net.stop()