import socket
import json
from _thread import start_new_thread
from GameController import GameController
from chatDatabase import chatDatabase


# Set up server address and port
server = "localhost"
port = 5555

# Create a socket object that enable reuse
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the server address and port
try:
    s.bind((server, port))

    # Listen for incoming connections
    s.listen(6)
    print("Waiting for a connection, Server Started")

    # Define available characters and selected characters lists
    available_characters = ["Miss Scarlet", "Col. Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    selected_characters = []

    # List to store client connections
    connections = []


    # Function to handle each client connection
    def threaded_client(conn, player_id, game_controller: GameController, chat_database: chatDatabase):
        global connections

        characters = [
            "Miss Scarlet",
            "Col. Mustard",
            "Mrs. White",
            "Mr. Green",
            "Mrs. Peacock",
            "Professor Plum",
        ]
        character_name = characters[player_id]

        # Send a connection message to the client
        conn.send(str.encode("Connected to server"))

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

                        else:
                            pass

                    elif reply.startswith("valid_moves"):
                        valid_moves, options = game_controller.valid_moves()
                        conn.send(str.encode(f"{str(valid_moves)};{str(options)}"))
                        print("Valid moves returned.")
                        print(f"Current turn: {game_controller.current_player}")

                    elif reply.startswith("get_current_turn"):
                        # Send current player back to client
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
                        print(f"get_player_cards is called")
                        player_cards = None
                        for player in game_controller.players:
                            if player.character == character_name:
                                print(f"Character name: {character_name}")
                                player_cards = player.cards
                        conn.send(str.encode(f"{player_cards}"))
                        print("Player cards returned.")

                    elif reply.startswith(f"execute_move"):
                        move = reply.split(";")[1]
                        option = reply.split(";")[2]
                        # print(f"Execute curr player: {game_controller.current_player}")

                        # send message to all clients to update game board
                        # print(f"move: {move}, option: {option}")
                        # Execute move
                        game_controller.execute_move(move, option, chat_database)
                        print("Move executed.")

                    elif reply.startswith("get_game_logs"):
                        messages = chat_database.get_chatDisplay_messages()
                        conn.send(str.encode(f"{messages}"))
                        print("Chat logs returned.")

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

    # Initialize global objects for use across all clients
    player_id = 0
    game_controller = GameController()
    game_controller.create_answer()
    chat_database = chatDatabase()

    # Main server loop
    while True:
        # Accept a new connection
        conn, addr = s.accept()
        print("Connected to:", addr)

        # Add the connection to the list
        connections.append(conn)

        # Start a new thread to handle the client connection
        start_new_thread(threaded_client, (conn, player_id, game_controller, chat_database))

        if player_id == 5:
            player_id = 0
        else:
            player_id += 1

except socket.error as e:
    # Print error and close socket
    print(str(e))
    s.close()


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
