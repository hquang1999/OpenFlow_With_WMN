import socket as sck
import threading

PORT = 5500
SERVER_IP = "192.168.1.113"
ADDR = (SERVER_IP, PORT)

# Creates the socket
server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
# Binds the socket to the ip and port #
server.bind(ADDR)

# Individual connection handler
def client_handler(connected_obj, address):
    pass

def server_side_handler():
    server.listen()
    while True:
        # This line is waiting for a new connection to the server
        # (object, IP and port)
        connected_obj, address = server.accept()
        # Thread for the client handler
        thread = threading.Thread(target=client_handler(),
                                  args=(connected_obj, address))
        thread.start()
        # Prints out active client threads
        print(f"[Active Connection] {threading.activeCount() - 1}")



print("[Starting] server socket is starting!")
server_side_handler()


