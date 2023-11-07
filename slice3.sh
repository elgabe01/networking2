#!/bin/sh


if [ -z "$1" ]
then
echo '---------- Creating Slice 3 ----------'
echo 'Switch 1:'
fi
sudo ovs-vsctl set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:3=@3q -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=4000000

if [ -z "$1" ]
then
echo 'Switch 3:'
fi
sudo ovs-vsctl set port s3-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:3=@3q -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=4000000 
if [ -z "$1" ]
then
echo '---------- End Creating Sice ----------'
fi

#mapping s1 queues to hosts (h1 - h6,h7)
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.6,idle_timeout=0,actions=set_queue:3,normal
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.7,idle_timeout=0,actions=set_queue:3,normal

#mapping s3 queues to hosts (h6 - h1,h7)
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.1,idle_timeout=0,actions=set_queue:3,normal
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.1,idle_timeout=0,actions=set_queue:3,normal
