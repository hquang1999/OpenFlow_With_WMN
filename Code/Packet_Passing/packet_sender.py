import socket as sck

FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MSG = "!!!DISCONNECT!!!"
PORT = 5500
# ADJUST THE SERVER IP
SERVER_IP = "192.168.1.113"
ADDR = (SERVER_IP, PORT)

# Connect to the server
client_socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
client_socket.connect(ADDR)

def send_handler(msg):
    # Encode into bytes sized object
    message = msg.encode(FORMAT)
    # Gets the message length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # This adds blank padding of sie HEADER - message length to make sure we are
    # always sending something of length HEADER
    send_length += b' ' * (HEADER - len(send_length))
    client_socket.send(send_length)
    client_socket.send(message)

send_handler("Hello World!")
send_handler(DISCONNECT_MSG)