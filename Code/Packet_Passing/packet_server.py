import scapy.all as scapy

def process_packet(packet):
    if (packet.haslayer(scapy.ICMP)):
        destination_mac = packet[0][0].src
        destination_ip = packet[0][1].src
        print(f"dst_IP = {destination_ip} | dst_MAC = {destination_mac}")

traffic = scapy.sniff(iface="wlp2s0", prn=process_packet, count=10)

test = scapy.packet
'''
traffic = scapy.sniff(iface="wlp2s0", count=5)
traffic.nsummary()
'''

