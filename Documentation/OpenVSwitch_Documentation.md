# Information

# Links

OpenVSwitch Manual:
[https://www.openvswitch.org//support/dist-docs/ovs-ofctl.8.txt](https://www.openvswitch.org//support/dist-docs/ovs-ofctl.8.txt)

OpenFlow Compatibility:
[https://docs.openvswitch.org/en/latest/faq/openflow/](https://docs.openvswitch.org/en/latest/faq/openflow/)

OVS with SDN:
[https://medium.com/@blackvvine/sdn-part-2-building-an-sdn-playground-on-the-cloud-using-open-vswitch-and-opendaylight-a0e2de029ce1](https://medium.com/@blackvvine/sdn-part-2-building-an-sdn-playground-on-the-cloud-using-open-vswitch-and-opendaylight-a0e2de029ce1)
# Commands

#### Installation
```
sudo apt install openvswitch-switch
```

#### Show All OpenVSwitch Options
```
sudo ovs-vsctl show
```

#### Create Bridge
```
sudo ovs-vsctl add-br <br_x>
```

#### Create Port (VTEP)
```
sudo ovs-vsctl add-port <br_x> <port_x> -- set Interface <port_x> type=[type] options:remote_ip=<remote_ip> options:keys=flow 
```
##### \[type\]
* internal: inside of the switch.
* vxlan: vlan connect, complication ethernet. Needs remote IP.
* gre: generic routing encapsulation, general purpose tunnel. Needs remote IP.

You can set the interface individually without add-port:
```
sudo ovs-vsctl set Interface <port_x> type=[type] options:remote_ip=<remote_ip> options:keys=flow 
```

#### Connect to Controller
```
sudo ovs-vsctl set-controller <br_x> tcp:<controller_ip>:<port>
```

#### IP Adding Shenanigans
This is for if you want to create a test port within the switch. You must create an internal port within the switch. type=internal, no remote_ip.
```
sudo ovs-vsctl add-br <br_x> <int_port> -- set Interface <int_port> type=internal
```

```
sudo ip addr add 192.168.1.1/24 dev <int_port>
sudo ifconfig <int_port> 192.168.1.1 netmask 255.255.255.0 up
route -n
```

#### Set Bridge Protocols
```
# Please check OVS version compatibility before doing all OpenFlow versions. At minimum, it should do OpenFlow13
sudo ovs-vsctl set bridge br_x protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13,OpenFlow14
```

#### Deletion
```
sudo ovs-vsctl del-br <br_x>
sudo ovs-vsctl del-port <br_x> <port_x>
```

#### Flushing Routing Table
```
sudo ip route flush table main
sudo reboot
```

### FULL SCRIPT
```
sudo ovs-vsctl del-br br_x
sudo ovs-vsctl add-br br_x

sudo ovs-vsctl add-port br_x p_xy -- set interface p_xy type=vxlan options:remote_ip=<ip of br_y> options:key=100 ofport_request=10

sudo ovs-vsctl set-controller br_x tcp:<controller ip>

sudo ovs-vsctl set bridge br_x protocols=OpenFlow13 

sudo ovs-vsctl show
```
### PROBE SCRIPT
```
sudo ovs-vsctl del-port br_x probe 
sudo ovs-vsctl add-port br_x probe -- set Interface probe type=internal

sudo ip addr add 50.50.50.x/24 dev probe
sudo ifconfig probe 50.50.50.x/24 mtu 1400 up

sudo ovs-vsctl show
```
#### Connecting Host to Bridge

OpenVSwitch is designed to connect virtual machines together across networks. It acts as an overlay switch/network. What we do is create a switch that will connect the VM or for this case, a simple tap port, to itself and establish a vxlan connection to the pi across the network. 

What VxLAN does is that it map's the tap port's ip with the underlying network ip, then it encapsulates the tap port's packets with the underlying network, essentially making that packet an underlying network packet. For this case, the underlying network will be B.A.T.M.A.N. The packet will be pushed to the other side where it exits the destination's VTEP, gets de-capsulated, then pushed up to the destination tap port. 

![](images/vxlan_encap.png)

[Image Source](https://medium.com/@blackvvine/sdn-part-2-building-an-sdn-playground-on-the-cloud-using-open-vswitch-and-opendaylight-a0e2de029ce1)
#### Topology Diagram

```
  Node 1 * {br_1} ------- (Port:10) ------- Node 2 * {br_2}
[Probe: 50.50.50.1]                       [Probe: 50.50.50.2]
[Bat0: 100.100.1.1]                       [Bat0: 100.100.1.2]
         |                                         |
         |                                         |
         |                                         |
     (Port:40)                                 (Port:20)
         |                                         |
         |                                         |
         |                                         |
  Node 4 * {br_4} ------- (Port:30) ------- Node 3 * {br_3}
[Probe: 50.50.50.4]                       [Probe: 50.50.50.3]
[Bat0: 100.100.1.4]                       [Bat0: 100.100.1.3]

Controller (OpenFlow13)
[Bat0: 100.100.1.5]
```
# OpenFlow Shenanigans
You will need to use this command to print OpenFlow descriptions based on the manual.
```
sudo ovs-ofctl -O OpenFlowV <setting> br_x
```
* OpenFlowV = OpenFlow versions, ie OpenFlow13
* \<setting\> are the settings provided by the manual
* br_x is the controller / bridge 

#### Flow Entry 
```
// ---- This one is the output flow ---- //
table=0,priority=1,in_port=1,ip,nw_src=50.50.50.1,nw_dst=50.50.50.2,actions=output:10
// ---- This one is the input flow ---- //
table=0,priority=1,in_port=10,ip,nw_src=50.50.50.2,nw_dst=50.50.50.1,actions=output:1
// ---- This one is for the controller ---- //
table=0,priority=0,actions=CONTROLLER:65535
```

10 is your vtep (p_21 as an example) port. 1 is your probe port. 