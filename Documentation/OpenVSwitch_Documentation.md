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
#### Create Port
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
sudo ovs-vsctl set bridge br_x protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
```

#### Full Script
```
sudo ovs-vsctl del-br br_x
sudo ovs-vsctl add-br br_x

sudo ovs-vsctl add-port br_x p_xy -- set interface p_xy type=[type] options:remote_ip=<ip of br_y> options:key=100

sudo ovs-vsctl set-controller br_x tcp:<controller ip>

sudo ovs-vsctl set bridge br_x protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13,OpenFlow14,OpenFlow15 

sudo ip link set br_x up

sudo ovs-vsctl show
```
#### Deletion
```
sudo ovs-vsctl del-br <br_x>
sudo ovs-vsctl del-port <br_x> <port_x>
```

#### Probe (GRE)
```
sudo ovs-vsctl del-port br_x probe 
sudo ovs-vsctl add-port br_x probe -- set Interface probe type=internal

sudo ip addr add 169.254.0.x/16 dev probe
sudo ifconfig probe 169.254.0.x/16 up

sudo ovs-vsctl show
```
#### Flushing Routing Table
```
sudo ip route flush table main
route -n
# restart PC
```
#### VxLAN Tunnel
```
sudo ip link add vxlan0 type vxlan id 100 dstport 4789 local <src_ip> remote <remote_ip>
sudo ip link set vxlan0 up
```

#### Topology Diagram

```
```
  Node 1 * {br_1} ------- (Key:100) ------- Node 2 * {br_2}
[Bat0: 100.100.1.1]                       [Bat0: 100.100.1.2]
[GRE: 169.254.0.10]                       [GRE: 169.254.0.20]
         |                                         |
         |                                         |
         |                                         |
         |                                         |
     (Key:400)                                 (Key:200)
         |                                         |
         |                                         |
         |                                         |
         |                                         |
  Node 4 * {br_4} ------- (Key:300) ------- Node 3 * {br_3}
[Bat0: 100.100.1.4]                       [Bat0: 100.100.1.3]
[GRE: 169.254.0.40]                       [GRE: 169.254.0.30]
 

Controller (OpenFlow14)
[Bat0: 100.100.1.5]
[GRE: None]
```
# OpenFlow Shenanigans
You will need to use this command to print OpenFlow descriptions based on the manual.
```
sudo ovs-ofctl -O OpenFlowV <setting> br_x
```
* OpenFlowV = OpenFlow versions, ie OpenFlow13
* \<setting\> are the settings provided by the manual
* br_x is the controller / bridge 
