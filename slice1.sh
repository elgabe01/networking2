#!/bin/sh


if [ -z "$1" ]
then
echo '---------- Creating Slice 1 ----------'
echo 'Switch 1:'
fi

sudo ovs-vsctl set port s1-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000

sudo ovs-vsctl set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000


if [ -z "$1" ]
then
echo 'Switch 2:'
fi
sudo ovs-vsctl set port s2-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000 

sudo ovs-vsctl set port s2-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000 


if [ -z "$1" ]
then
echo 'Switch 3:'
fi
sudo ovs-vsctl set port s3-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000 

sudo ovs-vsctl set port s3-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000

if [ -z "$1" ]
then
echo '---------- End Creating Sice ----------'
fi



#mapping s1 queues to hosts (h3 - h4,h6)
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.4,idle_timeout=0,actions=set_queue:3,normal
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.6,idle_timeout=0,actions=set_queue:3,normal

#mapping s2 queues to hosts (h4 - h3,h6)
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.3,idle_timeout=0,actions=set_queue:3,normal
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.6,idle_timeout=0,actions=set_queue:3,normal

#mapping s3 queues to hosts (h6 - h3,h4)
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.3,idle_timeout=0,actions=set_queue:3,normal
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.4,idle_timeout=0,actions=set_queue:3,normal
