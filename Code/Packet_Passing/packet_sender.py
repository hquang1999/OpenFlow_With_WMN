import socket as sck

FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MSG = "!!!DISCONNECT!!!"
PORT = 5500
# ADJUST THE SERVER IP
SERVER_IP = "192.168.1.113"
ADDR = (SERVER_IP, PORT)

client_socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
client_socket.connect(ADDR)