import scapy.all as scapy

traffic = scapy.sniff(iface="wlp2s0", filter="tcp", count=5)
traffic.nsummary()

