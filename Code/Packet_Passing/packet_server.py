import scapy.all as scapy

traffic = scapy.sniff(filter="tcp", count=5)


