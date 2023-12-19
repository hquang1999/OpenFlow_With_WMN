import scapy.all as scapy

def process_packet(packet):
    #packet.show()
    #destination_mac = packet[0][scapy.ETH_P_IP].dst
    #destination_ip = packet[0][scapy.IP_PROTOS].dst
    print(scapy.ETH_P_IP)


traffic = scapy.sniff(iface="wlp2s0", prn=process_packet, count=1)
'''
traffic = scapy.sniff(iface="wlp2s0", count=5)
traffic.nsummary()
'''

