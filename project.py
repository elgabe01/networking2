from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import udp
from ryu.lib.packet import tcp
from ryu.lib.packet import icmp
import subprocess
import threading 
import time

class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)

        # Destination Mapping [router --> MAC Destination --> Eth Port Output]
        self.mac_to_port = {
    1: {"00:00:00:00:00:01": 3, "00:00:00:00:00:02": 4, "00:00:00:00:00:03": 1, "00:00:00:00:00:04": 2,},
    2: {"00:00:00:00:00:05": 3, "00:00:00:00:00:06": 4, "00:00:00:00:00:07": 1, "00:00:00:00:00:08": 2,},
    3: {"00:00:00:00:00:09": 1, "00:00:00:00:00:0a": 2, "00:00:00:00:00:0b": 3, "00:00:00:00:00:0c": 4,},
        }
        
        
        self.print_flag = 0         # Helper variable that helps us with printing/output
          
        self.threadd = threading.Thread(target=self.inserimento, args=())
        self.threadd.daemon = True
        self.threadd.start()

        # Source Mapping   
        self.port_to_port = {
    1: { 1: 3, 2: 4, 3: 1, 4: 2,},
    2: { 1: 3, 2: 4, 3: 1, 4: 2,},
    3: { 1: 1, 2: 2, 3: 3, 4: 4,},
        }
        


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        
        dst = eth.dst
        src = eth.src
        
        dpid = datapath.id
        
        if dpid in self.mac_to_port:
                if dst in self.mac_to_port[dpid]:
                    out_port = self.mac_to_port[dpid][dst]
                    actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                    match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                    self.add_flow(datapath, 1, match, actions)
                    self._send_package(msg, datapath, in_port, actions)

                    
    def inserimento(self):
            active_slices = [False for _ in range(3)]
            while True:
                time.sleep(1)
                print("Inserisci: (es. ON 1, OFF 2)")
                var = input()
                splitString = var.split(" ")
                status = splitString[0]
                control=0
		
                if (status !='on' and status !='On' and status !='ON' and status !='off' and status !='Off' and status !='OFF' and status !='stat' and status !='Stat' and status !='STAT'):
                        print('Errore! Inserire ON o OFF')
                        continue
			
                if len(splitString)>1:
                        slice_number = int(splitString[1])
                        control=1
                        if slice_number < 1 or slice_number > 3:
                                print('Il numero di slice deve essere compreso tra 1 e 3')
                                continue

		
                if (status == 'ON' or status =='on' or status =='On'):
                        if control==1:
                                if slice_number == 1:
                                        print('        ***Activate Slice 1***                ')
                                        active_slices[0]=True;
                                        subprocess.call("./slice1.sh")
                                if slice_number == 2:
                                        print('        ***Activate Slice 2***                ')
                                        active_slices[1]=True;
                                        subprocess.call("./slice2.sh")
                                if slice_number == 3:
                                        print('        ***Activate Slice 3***                ')
                                        active_slices[2]=True;
                                        subprocess.call("./slice3.sh")
                        else:
                                print('        ***Activate All Slices***                ')
                                for i in range(len(active_slices)):
                                        str_slice = "./slice"
                                        if (not active_slices[i]):
                                                str_slice += str(i+1) + ".sh"
                                                active_slices[i] = True
                                                subprocess.call([str_slice])

                elif (status == 'OFF' or status =='off' or status =='Off'):
                        subprocess.call("./init_link.sh")
                        if control==0:
                                print('        ***De-Activate Slices***                ')
                                active_slices = [False for _ in range(3)]
                        else:
                                print('        ***De-Activate Slice ',slice_number,' ***                ')
                                active_slices[slice_number-1]=False
                                for i in range(len(active_slices)):
                                        str_slice="./slice"
                                        if active_slices[i]:
                                                str_slice += str(i+1) + ".sh"
                                                #print(str_slice)
                                                subprocess.call([str_slice, str(1)])
                
