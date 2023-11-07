from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import subprocess


class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."
         
        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        link_config = dict()
        host_link_config = dict()
 
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')


        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s2)
        self.addLink(h5, s2)
        self.addLink(h6, s3)
        self.addLink(h7, s3)

topos = { 'mytopo': ( lambda: MyTopo() ) }

if __name__ == "__main__":
    topo = MyTopo()
    net = Mininet(
        topo=topo,
        
        #specify an external controller by passing the Controller object in the Mininet constructor
        #controller=RemoteController( 'c0', ip='127.0.0.1'), 
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    controller = RemoteController('c0', ip='127.0.0.1', port=6633)
    net.addController(controller)
    
    net.build()
    net.start()

    subprocess.call("./init_link.sh")
    net.pingAll()
    CLI(net)

    net.stop()
