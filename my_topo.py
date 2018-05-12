import atexit
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

net = None 

class MyTopo(Topo):
	def __init__(self):
		Topo.__init__(self)

		s1 = self.addSwitch('s1')
		h1 = self.addHost('h1',ip='10.0.0.1')
		h2 = self.addHost('h2',ip='10.0.0.2')
		self.addLink(h1,s1,cls=TCLink, bw=100, delay='0ms', loss=0)
		self.addLink(h2,s1,cls=TCLink, bw=100, delay='0ms', loss=1)


def start_topo():
	global net
	print('Starting MyTopo...')
	setLogLevel('info')
	my_topo = MyTopo()
	net = Mininet(my_topo)
	net.start()
	net.pingAll()
	CLI(net)
	
def stop_topo():
	if(net is not None):
		info('*** Stoping net ***')
		net.stop()


if(__name__ == '__main__'):
	start_topo()
	atexit.register(stop_topo)
	
