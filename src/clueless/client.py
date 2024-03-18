#credit to https://www.youtube.com/watch?v=3QiPPX-KeSc&t=1054s

import socket

HEADER = 64 #defining starter number of bytes in message
PORT = 5050 #above port 4000
SERVER = socket.gethostbyname(socket.gethostname()) #gets IP address by name of computer
FORMAT = "utf-8"
DISCONNECT = "DISCONNECT!"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) #connect client to server


def send(msg):
    message = msg.encode(FORMAT) #encode string to bytes
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #pad message to starter length
    client.send(send_length)
    client.send(message)
    print(client.recv(2048)).decode(FORMAT)

