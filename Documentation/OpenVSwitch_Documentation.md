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
  Node 1 * {br_1} ------- (Key:100) ------- Node 2 * {br_2}
[Bat0: 100.100.1.1]                       [Bat0: 100.100.1.2]
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

#### Condensed Commands:
```
`admin@Leaf1$ovs-ofctl --help`

`ovs-ofctl: OpenFlow switch management utility`

`usage: ovs-ofctl [OPTIONS] COMMAND [ARG...]`

`For OpenFlow switches:`

  `show SWITCH                 show OpenFlow information`

  `dump-desc SWITCH            print switch description`

  `dump-tables SWITCH          print table stats`

  `dump-table-features SWITCH  print table features`

  `mod-port SWITCH IFACE ACT   modify port behavior`

  `mod-table SWITCH MOD        modify flow table behavior`

  `get-frags SWITCH            print fragment handling behavior`

  `set-frags SWITCH FRAG_MODE  set fragment handling behavior`

  `dump-ports SWITCH [PORT]    print port statistics`

  `dump-ports-desc SWITCH [PORT]  print port descriptions`

  `dump-flows SWITCH           print all flow entries`

  `dump-flows SWITCH FLOW      print matching FLOWs`

  `dump-aggregate SWITCH       print aggregate flow statistics`

  `dump-aggregate SWITCH FLOW  print aggregate stats for FLOWs`

  `queue-stats SWITCH [PORT [QUEUE]]  dump queue stats`

  `add-flow SWITCH FLOW        add flow described by FLOW`

  `add-flows SWITCH FILE       add flows from FILE`

  `mod-flows SWITCH FLOW       modify actions of matching FLOWs`

  `del-flows SWITCH [FLOW]     delete matching FLOWs`

  `replace-flows SWITCH FILE   replace flows with those in FILE`

  `diff-flows SOURCE1 SOURCE2  compare flows from two sources`

  `packet-out SWITCH IN_PORT ACTIONS PACKET...`

                              `execute ACTIONS on PACKET`

  `monitor SWITCH [MISSLEN] [invalid_ttl] [watch:[...]]`

                              `print packets received from SWITCH`

  `snoop SWITCH                snoop on SWITCH and its controller`

  `add-group SWITCH GROUP      add group described by GROUP`

  `add-groups SWITCH FILE       add group from FILE`

  `mod-group SWITCH GROUP      modify specific group`

  `del-groups SWITCH [GROUP]   delete matching GROUPs`

  `dump-group-features SWITCH  print group features`

  `dump-groups SWITCH [GROUP]  print group description`

  `dump-group-stats SWITCH [GROUP]  print group statistics`

  `queue-get-config SWITCH PORT  print queue information for port`

  `add-meter SWITCH METER      add meter described by METER`

  `mod-meter SWITCH METER      modify specific METER`

  `del-meter SWITCH METER      delete METER`

  `del-meters SWITCH           delete all meters`

  `dump-meter SWITCH METER     print METER configuration`

  `dump-meters SWITCH          print all meter configuration`

  `meter-stats SWITCH [METER]  print meter statistics`

  `meter-features SWITCH       print meter features`

`For OpenFlow switches and controllers:`

  `probe TARGET                probe whether TARGET is up`

  `ping TARGET [N]             latency of N-byte echos`
  `benchmark TARGET N COUNT    bandwidth of COUNT N-byte echos`

`SWITCH or TARGET is an active OpenFlow connection method.`

`Other commands:`

  `ofp-parse FILE              print messages read from FILE`

  `mod-temp-thresh SWITCH THRESHOLD  modify temperature threshold`

  `dump-temp-thresh SWITCH     print temperature threshold`

  `ofp-parse-pcap PCAP         print OpenFlow read from PCAP`

  `dump-tables-desc SWITCH     print tables description`

  `bundle SWITCH MSG           send bundle messages`

`Active OpenFlow connection methods:`

  `tcp:IP[:PORT]           PORT (default: 6633) at remote IP`

  `ssl:IP[:PORT]           SSL PORT (default: 6633) at remote IP`

  `unix:FILE               Unix domain socket named FILE`

`PKI configuration (required to use SSL):`

  `-p, --private-key=FILE  file with private key`

  `-c, --certificate=FILE  file with certificate for private key`

  `-C, --ca-cert=FILE      file with peer CA certificate`

`Daemon options:`

  `--detach                run in background as daemon`

  `--no-chdir              do not chdir to '/'`

  `--pidfile[=FILE]        create pidfile (default: /ovs/var/run/openvswitch/ovs-ofctl.pid)`

  `--overwrite-pidfile     with --pidfile, start even if already running`

`OpenFlow version options:`

  `-V, --version           display version information`

  `-O, --protocols         set allowed OpenFlow versions`

                          `(default: OpenFlow10, OpenFlow11, OpenFlow12, OpenFlow13, OpenFlow14)`

`Logging options:`

  `-vSPEC, --verbose=SPEC   set logging levels`

  `-v, --verbose            set maximum verbosity level`

  `--log-file[=FILE]        enable logging to specified FILE`

                           `(default: /ovs/var/log/openvswitch/ovs-ofctl.log)`

  `--syslog-target=HOST:PORT  also send syslog msgs to HOST:PORT via UDP`

`Other options:`

  `--strict                    use strict match for flow commands`

  `--readd                     replace flows that haven't changed`

  `-F, --flow-format=FORMAT    force particular flow format`

  `-P, --packet-in-format=FRMT force particular packet in format`

  `-m, --more                  be more verbose printing OpenFlow`

  `--timestamp                 (monitor, snoop) print timestamps`

  `-t, --timeout=SECS          give up after SECS seconds`

  `--sort[=field]              sort in ascending order`

  `--rsort[=field]             sort in descending order`

  `--unixctl=SOCKET            set control socket name`

  `-h, --help                  display this help message`

  `-V, --version               display version information`
```