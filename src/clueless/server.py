import socket
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
    print(str(e))

# Listen for incoming connections
s.listen(2)
print("Waiting for a connection, Server Started")

# Define available characters and selected characters lists
available_characters = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
selected_characters = []

# List to store client connections
connections = []

# Function to handle each client connection
def threaded_client(conn, player_id):
    global connections

    character_assignments = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    character_name = character_assignments[player_id]
    
    # Send a connection message to the client
    conn.send(str.encode("Connected to server"))

    while True:
        try:
            # Receive data from the client
            print("Waiting for data from client")  # Debug print
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            print(f"Received data: {reply}")  # Debug print

            if not data:
                print("Disconnected")
                break
            else:
                if reply.startswith("select_character:"):
                    # Extract the character name from the received message
                    character_name = reply.split(":")[1]
                    print(f"Character selected: {character_name}")  # Debug print

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
                            print("Lobby update sent to clients")  # Debug print
                elif reply.startswith("start_game"):
                    print("Game start button pressed")
                    for client in connections:
                        client.send(str.encode("Game has started."))
                        print("Game start message sent to clients")  # Debug print
                else:
                    print("Received: ", reply)
            print('REPLY: ', reply)
        except Exception as e:
            print("Error handling data from client:", e)
            break

    print("Lost connection")
    conn.close()

player_id = 0
# Main server loop
while True:
    # Accept a new connection
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Add the connection to the list
    connections.append(conn)

    # Start a new thread to handle the client connection
    start_new_thread(threaded_client, (conn, player_id))
    player_id += 1




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