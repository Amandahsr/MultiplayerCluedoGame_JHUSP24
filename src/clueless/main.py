import sys
import ast
from UI import UI, Button, PlayerCard, PlayerOptions, GameBoard, chatDisplay, CharacterIcon
from os import environ
from GameController import *

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import socket


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
        self.staticbuttons = []

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

    def main_menu(self):
        print("Start of main_menu function")  # Debug print
        
        # Display the main menu UI
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Welcome! Please select a character:", True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 4)

        # Initialize character buttons
        char_buttons = [
            Button(self.screen, "Miss Scarlet", 600, 500, "select_character"),
            Button(self.screen, "Col. Mustard", 600, 550, "select_character"),
            Button(self.screen, "Mrs. White", 600, 600, "select_character"),
            Button(self.screen, "Mr. Green", 600, 650, "select_character"),
            Button(self.screen, "Mrs. Peacock", 600, 700, "select_character"),
            Button(self.screen, "Professor Plum", 600, 750, "select_character"),
        ]
        self.buttons.extend(char_buttons)

        running = True
        while running:
            self.screen.fill((0, 0, 0))
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
                            print("Character selection sent to server")  # Debug print
                            character = button.msg
                            running = False
                            self.character_assignment(character)
                

            if (running):
                pygame.display.update()
        
        
    def character_assignment(self, character):
        # Assign characters to players
        print("Start of character_assignment function")
        
        # Display the character assignment UI
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Character Selection:", True, (255,255,255), (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 4)

        self.character = character

        character_text = font.render(character, True, (255,255,255), (0,0,0))
        characterRect = character_text.get_rect()
        characterRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)

        start_button = Button(self.screen, "Start Game", self.gameUI.screen_width // 2, self.gameUI.screen_height * 3 // 4, "")

        running = True
        while running:
            self.screen.fill((0,0,0))
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

            if (running):
                pygame.display.update()
    
    def main_game(self):
        pygame.init()
        
        # Initialize screen
        self.screen = pygame.display.set_mode((self.gameUI.screen_width, self.gameUI.screen_height), pygame.RESIZABLE)
        BLACK = (0, 0, 0)  
        clock = pygame.time.Clock()

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

        # Initialize player cards
        self.s.send(f"get_player_cards: {self.character}".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        available_cards = ast.literal_eval(server_msg)
        player_card = PlayerCard(self.gameUI, self.character, available_cards)

        # Initialize player options
        self.s.send("valid_moves".encode())
        server_msg = self.s.recv(1024).decode("utf-8")
        valid_moves = ast.literal_eval(server_msg.split(";")[0])
        options = server_msg.split(";")[1]
        player_options = PlayerOptions(self.gameUI, valid_moves, self.screen)

        # Initialize chat log display
        chat_display = chatDisplay(self.screen, chat_display_rect.x + chat_display_rect.width // 2,
                                    chat_display_rect.y + chat_display_rect.height // 2)
        chat_display.rect = chat_display_rect   

        pygame.display.update()             

        # # Create a positions data structure
        # positions = {
        #     'player1': (0, 0),
        #     'player2': (1, 0),
        #     # Add more positions as needed
        # }

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Drawing the different sections
            pygame.draw.rect(self.screen, BLACK, game_board_rect)
            pygame.draw.rect(self.screen, BLACK, chat_display_rect)
            pygame.draw.rect(self.screen, BLACK, player_card_rect)
            pygame.draw.rect(self.screen, BLACK, player_options_rect)

            # Redraw UI components onto their respective sections
            self.screen.fill(BLACK)
            game_board.draw(self.screen.subsurface(game_board_rect))
            chat_display.display_chat_messages()
            player_options.draw(self.screen.subsurface(player_options_rect))
            player_card.draw(self.screen.subsurface(player_card_rect))

            # Initialize player cards buttons
            start_y = 50
            for card in available_cards:
                self.staticbuttons.append(Button(self.screen, card, 900, start_y, ""))
                start_y += 10

            for button in self.staticbuttons:
                button.draw_button()

            # Initialize player options1 buttons #FIX BUTTON COORDINATE ISSUE#
            start_y = 500
            for move in valid_moves:
                self.buttons.append(Button(self.screen, str(move), 900, start_y, "show_options"))
                start_y += 50

            for button in self.buttons:
                button.draw_button()

            # Track which button is being pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.command_function == "show_options":
                            available_options = None
                            print(f"BUTTON MSG: {button.msg}")
                            if button.msg == "Move To Hallway":
                                available_options = options["Hallways"]
                            elif button.msg == "Move To Room and Suggest":
                                available_options = options["Rooms"]

                            move = button.msg
                            # Clear valid moves button
                            self.buttons = []

                            # Initialize player options2 buttons
                            start_y = 500
                            for option in available_options:
                                self.buttons.append(Button(self.screen, f"{move};{option}", 900, start_y, "execute_move"))
                                start_y += 50
                            for button in self.buttons:
                                button.draw_button()

                        elif button.check_button(mouse_x, mouse_y):
                            self.s.send(f"{button.command_function};{button.msg}".encode())
                            print("Start game message sent to server")  # Debug print
                            running = False
                    

            if (running):
                pygame.display.update()

            # Refresh the screen
            pygame.display.flip()
            clock.tick(30)  # Limit to 30 frames per second

        pygame.quit()

if __name__ == "__main__":
    client = Client()
