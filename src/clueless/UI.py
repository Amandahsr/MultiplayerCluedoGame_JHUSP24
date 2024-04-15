from os import environ
from collections import deque
import pygame

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


class UI:
    """A class to represent the user-interface settings of the client."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)


# class Text():
#     def __init__(self, screen, msg, x, y):

#             font = pygame.font.Font('freesansbold.ttf', 32)
#             text = font.render("Welcome! Please select a character:", True, (255,255,255), (0,0,0))
#             textRect = text.get_rect()
#             textRect.center = (gameUI.screen_width // 2, gameUI.screen_height // 2)
#             screen.blit(text, textRect)


class Button:
    msg = ""

    def __init__(self, screen, msg, x, y) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.msg = msg
        self.prep_msg(msg)

    def get_msg(self):
        return self.msg

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_button(self, x, y):
        if self.rect.collidepoint(x, y):
            return True

class PlayerCard:
    def __init__(self, gameUI, character_name, cards):
        self.character_name = str(character_name)  # Convert character_name to a string
        self.cards = cards
        self.gameUI = gameUI

    def display(self):
        print(f"Character: {self.character_name}")
        print("Cards: " + ", ".join(self.cards))

    def draw(self, surface):
        # Draw the player card on the surface
        # This is just a placeholder for now
        surface.fill((255, 255, 255))  # Fill the surface with white

        # Draw the player card header
        font = pygame.font.Font('freesansbold.ttf', 32)
        text_color = (0, 0, 0)  # Set the text color to black
        text = font.render(str(self.character_name), True, text_color)  # Convert self.character_name to a string
        text_rect = text.get_rect()
        text_rect.center = (self.gameUI.screen_width // 2, 50)
        surface.blit(text, text_rect)

class GameLog:
    def __init__(self, gameUI):
        self.actions = []
        self.gameUI = gameUI
    def add_entry(self, action):
        self.actions.append(action)
        if len(self.actions) > 5:
            self.actions.pop(0)

    def display(self):
        print("Game Log:")
        for action in reversed(self.actions[-5:]):
            print(action)

    def draw(self, surface):
        # Draw the game log on the surface
        # This is just a placeholder for now
        surface.fill((200, 200, 200))

        # Draw the game log header
        font = pygame.font.Font('freesansbold.ttf', 32)
        text_color = (0, 0, 0)  # Set the text color to black
        text = font.render("Game Log", True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (self.gameUI.screen_width // 2, 50)
        surface.blit(text, text_rect)

class PlayerOptions:
    def __init__(self, gameUI, options):
        self.options = options
        self.gameUI = gameUI

    def display(self):
        print("Options:")
        for option in self.options:
            print(option)

    def draw(self, surface):
        # Draw the game options on the surface
        # This is just a placeholder for now
        surface.fill((100, 100, 100))

        # Display the options as text
        font = pygame.font.Font('freesansbold.ttf', 32)
        text_color = (0, 0, 0)  # Set the text color to black
        text_y = 100  # Starting y-coordinate for the text

        # Draw the header text
        header_text = font.render("Player Options", True, text_color)
        header_rect = header_text.get_rect()
        header_rect.center = (self.gameUI.screen_width // 2, 50)
        surface.blit(header_text, header_rect)

        for option in self.options:
            text = font.render(option, True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (self.gameUI.screen_width // 2, text_y)
            surface.blit(text, text_rect)
            text_y += 50  # Increase y-coordinate for the next option

class GameBoard:
    def __init__(self, gameUI):
        #self.positions = positions
        self.gameUI = gameUI
        # Load the game board image
        original_image = pygame.image.load("Gameboard.png")
        
        img_width = self.gameUI.screen_width // 2
        img_height = self.gameUI.screen_height // 2
        self.image = pygame.transform.scale(original_image, (img_width, img_height))

    def update_position(self, character, position):
        self.positions[character] = position

    def display(self):
        print("Game Board:")
        for character, position in self.positions.items():
            print(f"{character} is at {position}")

    def draw(self, surface):
        # Draw the game board on the surface
        surface.fill((0, 0, 0))

        # Draw the game board image
        # Adjust (0, 0) to modify image position
        surface.blit(self.image, (0, 0))  

class chatDisplay:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 250, 100
        self.chat_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 20)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        # Maintain only maximum 5 messages
        self.messages = deque(["No log messages available."], maxlen=5)

    def add_chat_message(self, message: str):
        """
        Adds game log message into chatDisplay storage.
        """
        # Remove initial chat display message once game logs are available
        if "No log messages available" in self.messages:
            self.messages.clear()

        self.messages.appendleft(message)

    def display_chat_messages(self):
        """
        Draws updated chat display onto game screen.
        """
        # Draw chat display on screen
        pygame.draw.rect(self.screen, self.chat_color, self.rect)

        # Show log messages in chat display
        for index, msg in enumerate(self.messages):
            chat_surface = self.font.render(msg, True, self.text_color)

            # Calculate text coordinates in chat display
            text_x = self.rect.x + 10
            text_y = self.rect.y + 10 + (index * 30)
            self.screen.blit(chat_surface, (text_x, text_y))
