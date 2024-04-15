import sys
from UI import UI
from UI import Button
from UI import PlayerCard, GameLog, PlayerOptions, GameBoard
from UI import UI, Button, chatDisplay
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import socket


class Client:
    def __init__(self):
        pygame.init()
        self.gameUI = UI()
        self.screen = pygame.display.set_mode((self.gameUI.screen_width, self.gameUI.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Clue-Less")

        self.server = "localhost"
        self.port = 5555
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server, self.port))
            data = self.s.recv(1024).decode("utf-8")
            print(data)
        except KeyError as e:
            print("Failed to connect to server:", e)
            pygame.quit()
            sys.exit()

        # Display chat messages in bottom right
        self.chat_display = chatDisplay(self.screen, self.gameUI.screen_width - 50, self.gameUI.screen_height - 50)
        self.main_game()

    def main_menu(self):
        print("Start of main_menu function")  # Debug print
        
        # Display the main menu UI
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Welcome! Please select a character:", True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.gameUI.screen_width // 2, self.gameUI.screen_height // 4)

        buttons = [
            Button(self.screen, "Miss Scarlet", 600, 500),
            Button(self.screen, "Colonel Mustard", 600, 550),
            Button(self.screen, "Mrs. White", 600, 600),
            Button(self.screen, "Mr. Green", 600, 650),
            Button(self.screen, "Mrs. Peacock", 600, 700),
            Button(self.screen, "Professor Plum", 600, 750),
        ]

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, textRect)
            for button in buttons:
                button.draw_button()

            # Display chat messages
            self.chat_display.display_chat_messages()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.check_button(mouse_x, mouse_y):
                            self.s.send(f"select_character:{button.msg}".encode())
                            print("Character selection sent to server")  # Debug print
                            character = button.msg
                            running = False
                            self.character_assignment(character)

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

        start_button = Button(self.screen, "Start Game", self.gameUI.screen_width // 2, self.gameUI.screen_height * 3 // 4)

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
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if start_button.check_button(mouse_x, mouse_y):
                        self.s.send("start_game".encode())
                        print("Start game message sent to server")  # Debug print
                        running = False
                        self.main_game()

            pygame.display.update()
    
    def main_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.gameUI.screen_width, self.gameUI.screen_height), pygame.RESIZABLE)
        BLACK = (0, 0, 0)  
        WHITE = (255, 255, 255)

        clock = pygame.time.Clock()
        
        # Hard coded  for testing purposes
        self.character = "Miss Scarlet"

        # Will need to be updated to reflect the actual game state
        current_locations = {
            "Miss Scarlet": "HL_Hall",
            "Col. Mustard": "LD_Hall",
            "Mrs. White": "BK_Hall",
            "Mr. Green": "CB_Hall",
            "Mrs. Peacock": "LC_Hall",
            "Professor Plum": "SL_Hall"
        }

        options = ['Move', 'Suggest', 'Accuse']

        game_board = GameBoard(self.gameUI, current_locations)
        game_log = GameLog(self.gameUI)
        player_options = PlayerOptions(self.gameUI, options)
        player_card = PlayerCard(self.gameUI, self.character, ['Card 1', 'Card 2', 'Card 3'])

        # Define the rectangles for each section
        game_board_rect = pygame.Rect(0, 0, self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)
        game_log_rect = pygame.Rect(0, self.gameUI.screen_height // 2, self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)
        player_card_rect = pygame.Rect(self.gameUI.screen_width // 2, 0, self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)
        player_options_rect = pygame.Rect(self.gameUI.screen_width // 2, self.gameUI.screen_height // 2, self.gameUI.screen_width // 2, self.gameUI.screen_height // 2)

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Drawing the different sections
            pygame.draw.rect(self.screen, BLACK, game_board_rect)
            pygame.draw.rect(self.screen, BLACK, game_log_rect)
            pygame.draw.rect(self.screen, BLACK, player_card_rect)
            pygame.draw.rect(self.screen, BLACK, player_options_rect)

            # Drawing the UI components onto their respective sections
            game_board.draw(self.screen.subsurface(game_board_rect))
            game_log.draw(self.screen.subsurface(game_log_rect))
            player_options.draw(self.screen.subsurface(player_options_rect))
            player_card.draw(self.screen.subsurface(player_card_rect))

            # Refresh the screen
            pygame.display.flip()
            clock.tick(30)  # Limit to 30 frames per second

        pygame.quit()


if __name__ == "__main__":
    client = Client()



#     def lobby(self):
#         # Display the lobby UI and update selected characters
#         print("Start of lobby function")
#         start_button = Button(self.screen, "Start game", 600, 600)
#         running = True
#         while running:
# <<<<<<< client-debug
#             print("Start of While loop inside lobby function")  # Debug print
#             self.screen.fill((0,0,0))
            
#             # Add header text
#             header_font = pygame.font.Font('freesansbold.ttf', 40)
#             header_text = header_font.render("Pregame Lobby", True, (255,255,255), (0,0,0))
#             header_text_rect = header_text.get_rect()
#             header_text_rect.center = (self.gameUI.screen_width // 2, 50)
#             self.screen.blit(header_text, header_text_rect)
            
# =======
#             self.screen.fill((0, 0, 0))
# >>>>>>> main
#             try:
#                 print("Trying to receive data from server")  # Debug print
#                 data = self.s.recv(1024).decode("utf-8")
#                 print(f"Received data: {data}")  # Debug print
#                 if data.startswith("lobby_update:"):
#                     selected_characters = data.split(":")[1].split(",")
#                     print(f"Selected characters: {selected_characters}")  # Debug print
#                     y_pos = 100
#                     for character in selected_characters:
#                         text = pygame.font.Font("freesansbold.ttf", 20).render(
#                             character, True, (255, 255, 255), (0, 0, 0)
#                         )
#                         self.screen.blit(text, (100, y_pos))
#                         y_pos += 30
#                     if len(selected_characters) >= 2:
#                         start_button.draw_button()
#                         for event in pygame.event.get():
#                             if event.type == pygame.MOUSEBUTTONDOWN:
#                                 mouse_x, mouse_y = pygame.mouse.get_pos()
#                                 if start_button.check_button(mouse_x, mouse_y):
#                                     self.s.send("start_game".encode())
#                                     print("Start game button clicked")  # Debug print
#                                     running = False
#                                     self.main_game()
#             except KeyError as e:
#                 print("Failed to receive data from server:", e)

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     print("Quit event detected")  # Debug print
#                     running = False
#                     pygame.quit()
#                     sys.exit()

#             pygame.display.update()
#             print("Updated display - End of Lobby Function")  # Debug print