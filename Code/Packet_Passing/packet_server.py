import scapy.all as scapy
from scapy.all import *
def packet_server(packet):
    if IP in packet and UDP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        udp_payload = bytes(packet[Raw].load).decode('utf-8')

        print(f"Received packet from {src_ip} to {dst_ip}")
        print(f"Message: {udp_payload}")

    # Sniffing for UDP packets on port 12345

sniff(prn=packet_callback, filter="udp and port 12345")
'''
traffic = scapy.sniff(iface="wlp2s0", count=5)
traffic.nsummary()
'''

