import sys
import ast
import json
from UI import UI, Button, PlayerCard, PlayerOptions, GameBoard, chatDisplay, CharacterIcon
from os import environ
from GameController import *
import pygame
import socket
from debug import debug

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Client:
    def __init__(self):
        pygame.init()

        self.gameUI = UI()
        self.character = None
        self.screen = pygame.display.set_mode((self.gameUI.screen_width, self.gameUI.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Clue-Less")

        self.server = "localhost"
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.available_suspects = [
            "Miss Scarlet",
            "Col. Mustard",
            "Mrs. White",
            "Mr. Green",
            "Mrs. Peacock",
            "Professor Plum",
        ]
        self.available_weapons = ["Candlestick", "Wrench", "Knife", "Revolver", "Rope", "Lead Pipe"]
        self.available_rooms = [
            "Study",
            "Hall",
            "Lounge",
            "Library",
            "Billiard",
            "Dining",
            "Conversatory",
            "Ballroom",
            "Kitchen",
        ]

        # Tracks all buttons
        self.buttons = []
        self.buttons2 = []
        self.buttons_options = []

        try:
            self.s.connect((self.server, self.port))
            data = self.s.recv(1024).decode("utf-8")
            print(data)

        except KeyError as e:
            print("Failed to connect to server:", e)
            pygame.quit()
            sys.exit(0)

        self.main_menu()
        #self.end_game_tie()
        #self.end_game_win("Miss Scarlet")

    # def clear_server_msgs(self):
    #     while self.s.recv(1024):
    #         pass

    def check_turn(self):
        self.s.send("get_current_turn".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        return server_msg == self.character

    def main_menu(self):
        # print("Start of main_menu function")  # Debug print

        # Display the main menu UI
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Welcome! Please select a character:", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 4)

        # Initialize character buttons
        char_buttons = [
            Button(self.screen, BLACK, "Miss Scarlet", 600, 500, "select_character"),
            Button(self.screen, BLACK, "Col. Mustard", 600, 550, "select_character"),
            Button(self.screen, BLACK, "Mrs. White", 600, 600, "select_character"),
            Button(self.screen, BLACK, "Mr. Green", 600, 650, "select_character"),
            Button(self.screen, BLACK, "Mrs. Peacock", 600, 700, "select_character"),
            Button(self.screen, BLACK, "Professor Plum", 600, 750, "select_character"),
        ]
        self.buttons.extend(char_buttons)

        running = True
        while running:
            self.screen.fill(BLACK)
            self.screen.blit(text, textRect)

            self.s.send("get_available_characters".encode())
            server_msg = self.s.recv(1024).decode("utf-8")
            avail_characters = json.loads(server_msg)
            #print(f"Available characters: {avail_characters}")

            if "Miss Scarlet" in avail_characters:
                char_buttons[0].draw_button()
            if "Col. Mustard" in avail_characters:
                char_buttons[1].draw_button()
            if "Mrs. White" in avail_characters:
                char_buttons[2].draw_button()
            if "Mr. Green" in avail_characters:
                char_buttons[3].draw_button()
            if "Mrs. Peacock" in avail_characters:
                char_buttons[4].draw_button()
            if "Professor Plum" in avail_characters:
                char_buttons[5].draw_button()

            # for button in self.buttons:
            #     button.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit(0)

                # Sends info on which button is being clicked to server
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for button in self.buttons:
                        if button.check_button(mouse_x, mouse_y):
                            if button.msg in avail_characters:
                                self.s.send(f"{button.command_function}:{button.msg}".encode())
                                print(f"{button.msg} selection sent to server")  # Debug print
                                character = button.msg
                                running = False
                                self.lobby(character)
                            

            if running:
                pygame.display.update()

    def lobby(self, character):
        print("Start of lobby scene")

        self.character = character

        # Display the character assignment UI
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Your Selected Character", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 4)
        character_text = font.render(character, True, WHITE, BLACK)
        characterRect = character_text.get_rect()
        characterRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)

        # Render start button
        start_button = Button(
            self.screen, BLACK, "Start Game", self.gameUI.screen_width // 2, self.gameUI.screen_height * 3 // 4, ""
        )

        running = True
        while running:
            self.screen.fill(BLACK)
            self.screen.blit(text, textRect)
            self.screen.blit(character_text, characterRect)
            
            # Draw start button if there are at least 3 players
            self.s.send("get_num_players".encode())
            num_players = int(self.s.recv(1024).decode("utf-8"))
            if num_players >= 3:
                start_button.draw_button()

            self.s.send("check_start".encode())
            server_msg = self.s.recv(1024).decode("utf-8")
            if server_msg == "true, start game":
                running = False
                self.buttons = []
                self.main_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if start_button.check_button(mouse_x, mouse_y):
                        self.s.send("start_game".encode())
                        # print("Start game message sent to server")  # Debug print
                        running = False

                        # Clear main menu buttons
                        self.buttons = []

                        # Start main game
                        self.main_game()

            if running:
                pygame.display.update()

    def main_game(self):
        # print("Start of main gameplay scene")
        pygame.init()
        self.buttons = []

        """
        Initializing game objects
        """
        # Initialize screen
        self.screen = pygame.display.set_mode((self.gameUI.screen_width, self.gameUI.screen_height), pygame.RESIZABLE)
        clock = pygame.time.Clock()

        # Initializing game board
        self.s.send("get_current_players".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        #print(f"Message received: {server_msg}")
        locations = ast.literal_eval(server_msg)
        game_board = GameBoard(self.gameUI, locations)

        # Subsection screen into 4 parts
        half_width = self.gameUI.screen_width // 2
        half_height = self.gameUI.screen_height // 2
        game_board_rect = pygame.Rect(0, 0, half_width, half_height)
        chat_display_rect = pygame.Rect(0, half_height, half_width, half_height)
        player_card_rect = pygame.Rect(half_width, 0, half_width, half_height)
        player_options_rect = pygame.Rect(half_width, half_height, half_width, half_height)

        # Obtain player cards from server
        self.s.send(f"get_player_cards: {self.character}".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        available_cards = ast.literal_eval(server_msg)
        player_card = PlayerCard(self.gameUI, self.character, available_cards)
        player_options = PlayerOptions(self.gameUI, [""], self.screen)

        pygame.display.update()

        """
        Game loop
        """
        # Keep track of game status and if a move button has been clicked
        running = True
        buttons1_showed = False
        options_showed = False
        show_buttons2_button = False
        show_options_button = False

        # Game loop
        while running:
            # Check whether it is current player's turn
            is_turn = self.check_turn()

            """
            Rendering game graphics
            """
            # Draw four sections
            pygame.draw.rect(self.screen, BLACK, game_board_rect)
            pygame.draw.rect(self.screen, BLACK, chat_display_rect)
            pygame.draw.rect(self.screen, BLACK, player_card_rect)
            pygame.draw.rect(self.screen, BLACK, player_options_rect)

            # Draw player options and cards
            self.screen.fill(BLACK)
            player_options.draw(self.screen.subsurface(player_options_rect))
            player_card.draw(self.screen.subsurface(player_card_rect))

            # Check if game is over
            self.s.send("check_game_over".encode())
            server_msg = self.s.recv(1024).decode("utf-8")
            #print(f"Server message: {server_msg}")
            if server_msg.split(":")[0] == "winner":
                winner = server_msg.split(":")[1]
                self.end_game_win(winner)
            elif server_msg == "tie":
                self.end_game_tie()

            # Get current players to draw gameboard
            self.s.send("get_current_players".encode())
            server_msg = self.s.recv(1024).decode("utf-8")
            locations = ast.literal_eval(server_msg)
            game_board = GameBoard(self.gameUI, locations)
            game_board.draw(self.screen.subsurface(game_board_rect), locations)

            # Get valid moves for current player
            self.s.send("valid_moves".encode())
            server_msg = self.s.recv(1024).decode("utf-8")
            valid_moves = ast.literal_eval(server_msg.split(";")[0])
            options = ast.literal_eval(server_msg.split(";")[1])
            # print(f"Valid moves: {valid_moves}; Options: {options}")

            # Get recent log messages from chatDatabase and display in-game
            self.s.send("get_game_logs".encode())
            server_msg = self.s.recv(1024).decode("utf-8")
            log_msgs = ast.literal_eval(server_msg)
            chat_display = chatDisplay(
                chat_display_rect,
                self.screen,
                chat_display_rect.x + chat_display_rect.width // 2,
                chat_display_rect.y + chat_display_rect.height // 2,
                log_msgs,
            )
            chat_display.display_chat_messages()

            # Debugging overlay on display
            debug(pygame.mouse.get_pos())

            """
            Rendering moves buttons
            """
            # LAYER 1.1: Render available moves button
            if not buttons1_showed and not options_showed and is_turn:
                # Start afresh
                self.buttons = []
                self.buttons2 = []

                start_x = 900
                start_y = 500
                for move in valid_moves:
                    move_text = str(move)
                    self.buttons.append(
                        Button(
                            self.screen, player_options.screen_color, move_text, start_x, start_y, "show_options", BLACK
                        )
                    )
                    start_y += 50

                for button in self.buttons:
                    button.draw_button()

            # LAYER 1.2: Render buttons2 if LAYER 1.1 is already showed
            if buttons1_showed and not options_showed and is_turn:
                # Reset to avoid overlapping button coordinates
                self.buttons = []

                for button in self.buttons2:
                    button.draw_button()

                show_buttons2_button = True

            # LAYER 2: Render available options button after a move is selected
            if options_showed and is_turn:
                # Reset to avoid overlapping button coordinates
                self.buttons = []
                self.buttons2 = []

                for button in self.buttons_options:
                    button.draw_button()

                show_options_button = True

            # If it isn't the player's turn, display a message to wait
            elif not is_turn:
                start_x = 800
                start_y = 550
                position = (start_x, start_y)
                # Create a Pygame font object
                font = pygame.font.Font(None, 45)
                # Render the text
                text = font.render("Wait Your Turn", 1, BLACK)
                # Draw the text on the screen
                self.screen.blit(text, position)

            """
            Button click responses
            """
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit(0)

                # Button clicks
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Position of cursor
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Moves button is clicked and next layer of buttons is called on
                    for button in self.buttons:
                        if button.check_button(mouse_x, mouse_y):
                            # Move button is clicked
                            if button.command_function == "show_options":
                                # Extract options based on move clicked
                                if button.msg == "Move To Hallway":
                                    options_showed = True

                                    # Initialize available options buttons
                                    start_x = 900
                                    start_y = 500
                                    for option in options["Hallways"]:
                                        self.buttons_options.append(
                                            Button(
                                                self.screen,
                                                player_options.screen_color,
                                                option,
                                                start_x,
                                                start_y,
                                                f"execute_move;{button.msg}",
                                                BLACK,
                                            )
                                        )
                                        start_y += 50

                                elif button.msg == "Pass":
                                    # Execute option move
                                    self.s.send("execute_move;Pass; ".encode())

                                    # Obtain updated players locations
                                    self.s.send("get_current_players".encode())
                                    server_msg = self.s.recv(1024).decode("utf-8")
                                    locations = ast.literal_eval(server_msg)
                                    game_board.draw(self.screen.subsurface(game_board_rect), locations)

                                    # Reinitialize graphics for next player
                                    game_board = GameBoard(self.gameUI, locations)
                                    self.buttons = []
                                    self.buttons2 = []
                                    self.buttons_options = []
                                    options_showed = False
                                    buttons1_showed = False
                                    show_buttons2_button = False

                                elif button.msg == "Move To Room and Suggest":
                                    # Reset buttons to avoid rendering move buttons
                                    self.buttons = []
                                    buttons1_showed = True

                                    # Initialize room buttons
                                    start_x = 900
                                    start_y = 500
                                    for room in options["Rooms"]:
                                        self.buttons2.append(
                                            Button(
                                                self.screen,
                                                player_options.screen_color,
                                                room,
                                                start_x,
                                                start_y,
                                                f"show_suggest_suspects;{button.msg};{room}",
                                                BLACK,
                                            )
                                        )
                                        start_y += 50

                                elif button.msg == "Accuse":
                                    # Reset buttons to avoid rendering move buttons
                                    self.buttons = []
                                    self.buttons2 = []
                                    buttons1_showed = True
                                    options_showed = False

                                    # Initialize room buttons
                                    start_x = 900
                                    start_y = 500
                                    for room in self.available_rooms:
                                        self.buttons2.append(
                                            Button(
                                                self.screen,
                                                player_options.screen_color,
                                                room,
                                                start_x,
                                                start_y,
                                                f"show_suggest_suspects;{button.msg};{room}",
                                                BLACK,
                                            )
                                        )
                                        start_y += 50
                                        
#                                 elif button.msg == "Accuse":
#                                     print("Pressed Accuse button")
#                                     self.s.send("accuse".encode())
#                                     server_msg = self.s.recv(1024).decode("utf-8")
#                                     print(f"Server message: {server_msg}")
#                                     if server_msg.split(":")[0] == "winner":
#                                         winner = server_msg.split(":")[1]
#                                         self.end_game_win(winner)
#                                     else:
#                                         pass

                            # For start button
                            else:
                                self.s.send(f"{button.command_function};{button.msg}".encode())
                                print(f"{button.command_function}{button.msg} selection sent to server")  # Debug print

                    # Moves button is clicked and moves2 buttons are called on
                    if show_buttons2_button:
                        for button in self.buttons2:
                            if button.check_button(mouse_x, mouse_y):
                                if button.command_function.startswith("show_suggest_suspects"):
                                    # Reset buttons to avoid rendering move buttons
                                    self.buttons = []
                                    self.buttons2 = []

                                    move = button.command_function.split(";")[1]
                                    room = button.command_function.split(";")[2]

                                    # Initialize suspects buttons
                                    start_x = 900
                                    start_y = 500
                                    for suspect in self.available_suspects:
                                        self.buttons2.append(
                                            Button(
                                                self.screen,
                                                player_options.screen_color,
                                                suspect,
                                                start_x,
                                                start_y,
                                                f"show_suggest_weapons;{move};{room}",
                                                BLACK,
                                            )
                                        )
                                        start_y += 50

                                elif button.command_function.startswith("show_suggest_weapons"):
                                    options_showed = True
                                    buttons1_showed = True

                                    # Reset buttons to avoid rendering move buttons
                                    self.buttons = []
                                    self.buttons2 = []
                                    self.buttons_options = []

                                    move_selected = button.command_function.split(";")[1]
                                    room = button.command_function.split(";")[2]
                                    suspect_selected = button.msg

                                    # Initialize weapons buttons
                                    start_x = 900
                                    start_y = 500
                                    for weapon in self.available_weapons:
                                        self.buttons_options.append(
                                            Button(
                                                self.screen,
                                                player_options.screen_color,
                                                weapon,
                                                start_x,
                                                start_y,
                                                f"execute_with_suggestion;{move_selected};{room};{suspect_selected};{weapon}",
                                                BLACK,
                                            )
                                        )
                                        start_y += 50

                    # Options button is clicked and execute move is called on
                    if show_options_button:
                        for button in self.buttons_options:
                            if button.check_button(mouse_x, mouse_y):
                                # Include suggestion msg for suggest moves
                                if button.command_function.startswith("execute_with_suggestion"):
                                    # Execute option move
                                    self.s.send(button.command_function.encode())

                                    # Obtain updated players locations
                                    self.s.send("get_current_players".encode())
                                    server_msg = self.s.recv(1024).decode("utf-8")
                                    locations = ast.literal_eval(server_msg)
                                    game_board.draw(self.screen.subsurface(game_board_rect), locations)

                                    # Reinitialize graphics for next player
                                    game_board = GameBoard(self.gameUI, locations)
                                    options_showed = False
                                    buttons1_showed = False
                                    show_options_button = False
                                    show_buttons2_button = False
                                    self.buttons = []
                                    self.buttons2 = []
                                    self.buttons_options = []

                                # Do not include suggestion for other moves
                                elif button.command_function.startswith("execute_move"):
                                    # Execute option move
                                    self.s.send(f"{button.command_function};{button.msg}".encode())

                                    # Obtain updated players locations
                                    self.s.send("get_current_players".encode())
                                    server_msg = self.s.recv(1024).decode("utf-8")
                                    locations = ast.literal_eval(server_msg)
                                    game_board.draw(self.screen.subsurface(game_board_rect), locations)

                                    # Reinitialize graphics for next player
                                    game_board = GameBoard(self.gameUI, locations)
                                    options_showed = False
                                    buttons1_showed = False
                                    show_options_button = False
                                    show_buttons2_button = False
                                    self.buttons = []
                                    self.buttons2 = []
                                    self.buttons_options = []

            if running:
                pygame.display.update()

            # Refresh screen
            # pygame.display.flip()
            clock.tick(30)  # Limit to 30 frames per second

        pygame.quit()

    def end_game_win(self, winner_name):
        print("End Game Win Scene Started")
        
        # Display the end game scene
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("We Have a Winner!", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 4)
        character_text = font.render(f"Congratulations {winner_name}", True, WHITE, BLACK)
        characterRect = character_text.get_rect()
        characterRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)
        gameover_text = font.render("Game Over", True, WHITE, BLACK)
        gameoverRect = gameover_text.get_rect()
        gameoverRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 1.3)

        running = True
        while running:
            self.screen.fill(BLACK)
            self.screen.blit(text, textRect)
            self.screen.blit(character_text, characterRect)
            self.screen.blit(gameover_text, gameoverRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit(0)

            if running:
                pygame.display.update()

    def end_game_tie(self):
        print("End Game Tie Scene Started")
        
        # Display the end game scene
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("This Game Has No Winner", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 4)
        character_text = font.render(f"Game Over", True, WHITE, BLACK)
        characterRect = character_text.get_rect()
        characterRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)

        running = True
        while running:
            self.screen.fill(BLACK)
            self.screen.blit(text, textRect)
            self.screen.blit(character_text, characterRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit(0)

            if running:
                pygame.display.update()


if __name__ == "__main__":

    client = Client()
