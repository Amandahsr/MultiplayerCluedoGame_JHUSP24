import socket
import threading

HEADER = 64 #defining starter number of bytes in message
PORT = 5050 #above port 4000
SERVER = socket.gethostbyname(socket.gethostname()) #gets IP address by name of computer
ADDR = (SERVER, PORT) #needs to be in a touple for binding
FORMAT = "utf-8"
DISCONNECT = "DISCONNECT!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #family, type. what type of IP address need, IPv4
server.bind(ADDR) #bound socket to address

def handle_client(conn, addr): #handles communciation between client and server
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        message_length = conn.recv(HEADER).decode(FORMAT) #receving number of bytes message will be
        if message_length: #if message not None
            message_length = int(message_length)
            message = conn.recv(message_length).decode(FORMAT) #receving message from socket
            print(f"{addr} {message}")
            if message == DISCONNECT:
                break

            print(f"[{addr}] {message}")
            conn.send("Msg received".encode(FORMAT))
    
    conn.close() #disconnect

def start():
    server.listen()
    print("[LISTENING] Server is listening on " + SERVER)
    while True:
        conn, addr = server.accept() #waiting for new connection to server
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #passing new connection to handle client
        thread.start()

print("[STARTING]")
start()
