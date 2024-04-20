import sys
import ast
import json
from UI import UI, Button, PlayerCard, PlayerOptions, GameBoard, chatDisplay, CharacterIcon
from os import environ
from GameController import *
import pygame
import socket
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

        # Tracks all buttons
        self.buttons = []
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

    # def clear_server_msgs(self):
    #     while self.s.recv(1024):
    #         pass
    
    def check_turn(self):
        self.s.send("get_current_turn".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        return server_msg == self.character

    def main_menu(self):
        print("Start of main_menu function")  # Debug print

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
            for button in self.buttons:
                button.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit(0)

                # Sends info on which button is being clicked to server
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    for button in self.buttons:
                        if button.check_button(mouse_x, mouse_y):
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
            start_button.draw_button()

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
                        print("Start game message sent to server")  # Debug print
                        running = False

                        # Clear main menu buttons
                        self.buttons = []

                        # Start main game
                        self.main_game()

            if running:
                pygame.display.update()

    def main_game(self):
        print("Start of main gameplay scene")
        pygame.init()

        # Initialize screen
        self.screen = pygame.display.set_mode((self.gameUI.screen_width, self.gameUI.screen_height), pygame.RESIZABLE)
        clock = pygame.time.Clock()
        chat_msg = None
        curr_move = None

        # Initializing game board
        self.s.send("get_current_players".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        print(f"Message received: {server_msg}")
        current_locations = ast.literal_eval(server_msg)
        game_board = GameBoard(self.gameUI, current_locations)

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
        print(f"Player cards: {available_cards}")

        # Obtain valid player moves/options from server
        self.s.send("valid_moves".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        valid_moves = ast.literal_eval(server_msg.split(";")[0])
        options = ast.literal_eval(server_msg.split(";")[1])
        player_options = PlayerOptions(self.gameUI, valid_moves, self.screen)
        print(f"Valid moves: {valid_moves}; Options: {options}")

        # Initialize chat log display
        chat_display = chatDisplay(
            self.screen,
            chat_display_rect.x + chat_display_rect.width // 2,
            chat_display_rect.y + chat_display_rect.height // 2,
        )
        chat_display.rect = chat_display_rect

        pygame.display.update()

        # Keep track of game status and if a move button has been clicked
        running = True
        options_showed = False

        # Check if this player has the current turn
        is_turn = self.check_turn()
        print(f"It is your turn: {is_turn}") 

        # Game loop
        while running:
            self.buttons = []

            # Draw four sections
            pygame.draw.rect(self.screen, BLACK, game_board_rect)
            pygame.draw.rect(self.screen, BLACK, chat_display_rect)
            pygame.draw.rect(self.screen, BLACK, player_card_rect)
            pygame.draw.rect(self.screen, BLACK, player_options_rect)

            # Draw game components into their respective sections
            self.screen.fill(BLACK)
            game_board.draw(self.screen.subsurface(game_board_rect))
            chat_display.display_chat_messages()
            player_options.draw(self.screen.subsurface(player_options_rect))
            player_card.draw(self.screen.subsurface(player_card_rect))

            # Render available moves button
            if not options_showed and is_turn:
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

            # Render available options button after a move is selected
            elif options_showed and is_turn:
                for button in self.buttons_options:
                    button.draw_button()
            
            # If it isn't the player's turn, display a message to wait
            else:
                start_x = 800
                start_y = 550
                position = (start_x, start_y)
                # Create a Pygame font object
                font = pygame.font.Font(None, 45)
                # Render the text
                text = font.render("Wait Your Turn", 1, BLACK)
                # Draw the text on the screen
                self.screen.blit(text, position)
                
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    print("Quit event detected")
                    running = False
                    pygame.quit()
                    sys.exit(0)

                # Button clicks
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse click registered")
                    # Position of cursor
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Find button that matches cursor coordinates
                    for button in self.buttons:
                        if button.check_button(mouse_x, mouse_y):
                            # Move button is clicked
                            if button.command_function == "show_options":
                                available_options = []
                                options_showed = True
                                curr_move = button.msg

                                # Extract options based on move clicked
                                if button.msg == "Move To Hallway":
                                    print("Move to Hallway registered")
                                    available_options.append(options["Hallways"])

                                elif button.msg == "Move To Room and Suggest":
                                    available_options.append(options["Rooms"])

                                # Initialize available options buttons
                                start_x = 900
                                start_y = 500
                                for option in available_options:
                                    self.buttons_options.append(
                                        Button(
                                            self.screen,
                                            player_options.screen_color,
                                            option,
                                            start_x,
                                            start_y,
                                            "execute_move",
                                            BLACK,
                                        )
                                    )
                                    start_y += 50

                            # For start button
                            else:
                                self.s.send(f"{button.command_function};{button.msg}".encode())
                                print(f"{button.command_function}{button.msg} selection sent to server")  # Debug print

                    # Options button is clicked
                    for button in self.buttons_options:
                        if button.check_button(mouse_x, mouse_y):
                            self.s.send(f"{button.command_function};{curr_move};{button.msg}".encode())
                            print(f"{button.command_function};{curr_move};{button.msg} sent to server")  # Debug print
                            
                            self.buttons_options = []
                            options_showed = False

                            # Receive game state change message
                            chat_msg = self.s.recv(1024).decode("utf-8")

                            # Update game board with new position after game state change
                            game_board.draw(self.screen.subsurface(game_board_rect))

                            # Update chat log display
                            if chat_msg:
                                chat_display.add_chat_message(server_msg)
                                chat_msg = None

            if running:
                pygame.display.update()

            # Refresh screen
            pygame.display.flip()
            clock.tick(150)  # Limit to 30 frames per second

        pygame.quit()


if __name__ == "__main__":
    client = Client()
