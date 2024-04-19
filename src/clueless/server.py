import socket
import json
from _thread import start_new_thread
from GameController import GameController
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
s.listen(6)
print("Waiting for a connection, Server Started")

# Define available characters and selected characters lists
available_characters = ["Miss Scarlet", "Col. Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
selected_characters = []

# List to store client connections
connections = []


# Function to handle each client connection
def threaded_client(conn, player_id, game_controller: GameController):
    global connections

    character_assignments = [
        "Miss Scarlet",
        "Col. Mustard",
        "Mrs. White",
        "Mr. Green",
        "Mrs. Peacock",
        "Professor Plum",
    ]
    character_name = character_assignments[player_id]

    # Send a connection message to the client
    conn.send(str.encode("Connected to server"))

    # # Send the character name to the client
    # conn.send(str.encode(character_name))

    while True:
        try:
            # Receive data from the client
            print("Waiting for data from client")  # Debug print
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            print(f"Received: {reply}")  # Debug print

            if not data:
                print("Disconnected")
                connections.remove(conn)
                conn.close()
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
                        game_controller.initialize_player(character_name)

                elif reply.startswith("start_game"):
                    print("Game start button pressed")
                    if not game_controller.initialized:
                        print("Initializing cards and turns")
                        game_controller.initialize_cards()
                        game_controller.initialize_turns()
                        game_controller.initialized = True
                    #for client in connections:
                    #conn.send(str.encode("proceed_to_main_game"))
                    #print(f"proceed_to_main_game sent to {conn}")
                    else:
                        pass

                elif reply.startswith("valid_moves"):
                    valid_moves, options = game_controller.valid_moves()
                    conn.send(str.encode(f"{str(valid_moves)};{str(options)}"))
                    print("Valid moves returned.")
                    print(f"Current turn: {game_controller.current_player}")

                elif reply.startswith("get_current_turn"):
                    conn.send(str(game_controller.current_player).encode())
                    print("Current turn returned.")

                elif reply.startswith("get_current_players"):
                    current_locations = {}
                    for player in game_controller.players:
                        current_locations[player.character] = player.location
                    current_locations = json.dumps(current_locations)
                    conn.send(current_locations.encode())
                    print("Current locations of players returned.")

                elif reply.startswith(f"get_player_cards: {character_name}"):
                    player_cards = None
                    for player in game_controller.players:
                        if player.character == character_name:
                            player_cards = player.cards
                    conn.send(str.encode(f"{player_cards}"))
                    print("Current locations of players returned.")

                elif reply.startswith(f"execute_move"):
                    print(f"Execute move: {reply}")
                    move = reply.split(";")[1]
                    option = reply.split(";")[2]
                    option = json.dumps(option)

                    # Execute move
                    game_controller.execute_move(move, option)

                    # Send game state change message back
                    conn.send(str.encode(game_controller.chat_msg))
                    print("Current locations of players returned.")

                else:
                    print("Received: ", reply)

        except KeyError as e:
            print("Error handling data from client:", e)
            break
        except ConnectionResetError as e:
            print("Connection reset by client")
            connections.remove(conn)
            conn.close()
            break

    print("Lost connection")
    # conn.close()


player_id = 0
game_controller = GameController()
game_controller.create_answer()

# Main server loop
while True:
    # Accept a new connection
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Add the connection to the list
    connections.append(conn)

    # Start a new thread to handle the client connection
    start_new_thread(threaded_client, (conn, player_id, game_controller))
    player_id += 1


"""
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
"""
