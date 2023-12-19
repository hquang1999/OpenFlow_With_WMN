from scapy.all import *

packet = IP(dst='192.168.1.15')/ICMP()
send(packet)

'''
traffic = scapy.sniff(iface="wlp2s0", count=5)
traffic.nsummary()
'''

