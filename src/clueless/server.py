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
=======
from _thread import *
import sys


# Set up server address and port
server = "localhost"
port = 5555

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Listen for incoming connections
s.listen(2)
print("Waiting for a connection, Server Started")

# Define available characters and selected characters lists
available_characters = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
selected_characters = []

# List to store client connections
connections = []

# Function to handle each client connection
def threaded_client(conn):
    global available_characters, selected_characters

    # Send a connection message to the client
    conn.send(str.encode("Connected to server"))

    while True:
        try:
            # Receive data from the client
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                if reply.startswith("select_character:"):
                    # Extract the character name from the received message
                    character_name = reply.split(":")[1]

                    # Check if the character is available
                    if character_name in available_characters:
                        # Remove the character from the available list
                        available_characters.remove(character_name)
                        # Add the character to the selected list
                        selected_characters.append(character_name)
                        print(f"{character_name} has been selected.")

                        # Prepare a lobby update message with the selected characters
                        lobby_update = "lobby_update:" + ",".join(selected_characters)

                        # Send the lobby update message to all connected clients
                        for client in connections:
                            client.send(str.encode(lobby_update))
                else:
                    print("Received: ", reply)
            print('REPLY: ', reply)
        except Exception as e:
            print("Error handling data from client:", e)
            break

    print("Lost connection")
    conn.close()

# Main server loop
while True:
    # Accept a new connection
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Add the connection to the list
    connections.append(conn)

    # Start a new thread to handle the client connection
    start_new_thread(threaded_client, (conn,))


'''
class Server:
    game_board = {
        "Study_Room": [],
        "SH_Hall": [],
        "Hall_Room": [],
        "HL_Hall": [],
        "Lounge_Room": [],
        "SL_Hall": [],
        "Library_Room": [],
        "LB_Hall": [],
        "Billiard_Room": [],
        "BD_Hall": [],
        "Dining_Room": [],
        "LC_Hall": [],
        "Conservatory_Room": [],
        "CB_Hall": [],
        "Ball_Room": [],
        "BK_Hall": [],
        "Kitchen_Room": []
    }

    def __init__(self):
        ProfPlum = Player('Prof. Plum')
        self.game_board['SL_Hall'] = [str(ProfPlum)]
        
        MrsPeacock = Player('Mrs. Peacock')
        self.game_board['LC_Hall'] = [str(MrsPeacock)]

        MrGreen = Player('Mr. Green')
        self.game_board['CB_Hall'] = [str(MrGreen)]

        MrsWhite = Player('Mrs. White')
        self.game_board['BK_Hall'] = [str(MrsWhite)]

        ColMustard = Player('Col. Mustard')
        self.game_board['LD_Hall'] = [str(ColMustard)]

        MissScarlet = Player('Miss Scarlet')
        self.game_board['HL_Hall'] = [str(MissScarlet)]
        
        print(self.game_board)
'''
