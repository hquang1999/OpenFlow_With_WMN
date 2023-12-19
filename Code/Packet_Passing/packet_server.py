import scapy.all as scapy

def process_packet(packet):
    packet.show()

traffic = scapy.sniff(iface="wlp2s0", prn=process_packet, count=1)
'''
traffic = scapy.sniff(iface="wlp2s0", count=5)
traffic.nsummary()
'''

