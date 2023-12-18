import scapy.all as scapy

def server_packet_handler(packet):
    if packet.haslayer(Raw):
        data = packet[Raw].load.decode('utf-8')
        print(f"Server received: {data}")

# Start the server and sniff packets
sniff(prn=server_packet_handler, store=0, filter="tcp port 12345")