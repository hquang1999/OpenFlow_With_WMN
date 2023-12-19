import scapy.all as scapy

def process_packet(packet):
    #packet.show()
    destination_mac = packet[0][0].dst
    destination_ip = packet[0][1].dst
    print(f"dst_IP = {destination_ip} | dst_MAC = {destination_mac}")


traffic = scapy.sniff(iface="wlp2s0", prn=process_packet, count=1)
'''
traffic = scapy.sniff(iface="wlp2s0", count=5)
traffic.nsummary()
'''

