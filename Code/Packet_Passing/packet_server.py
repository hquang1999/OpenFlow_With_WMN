import scapy.all as scapy

traffic = scapy.sniff(iface="ens6", count=5)
traffic.nsummary()