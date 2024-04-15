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
        self.header_font = pygame.font.Font('freesansbold.ttf', 28)
        self.card_font = pygame.font.Font('freesansbold.ttf', 25)
        self.text_color = (0, 0, 0)

    def display(self):
        print(f"Character: {self.character_name}")
        print("Cards: " + ", ".join(self.cards))

    def draw(self, surface):
        # Draw the player card on the surface
        # This is just a placeholder for now
        surface.fill((255, 255, 255))  # Fill the surface with white

        # Render header
        header_text = self.header_font.render(f"-- {self.character_name} CARDS --", True, self.text_color)
        header_rect = header_text.get_rect()
        header_rect.center = (surface.get_width() // 2, 15)
        surface.blit(header_text, header_rect)

        # Starting text location
        text_y = header_rect.bottom + 100

        # Render player cards
        for card in self.cards:
            text = self.card_font.render(card, True, self.text_color)
            text_rect = text.get_rect()
            text_rect.center = (surface.get_width() // 2, text_y)
            surface.blit(text, text_rect)
            text_y += 50


class PlayerOptions:
    def __init__(self, gameUI, options):
        self.options = options
        self.gameUI = gameUI
        self.header_font = pygame.font.Font('freesansbold.ttf', 28)
        self.option_font = pygame.font.Font('freesansbold.ttf', 25)

    def display(self):
        print("Options:")
        for option in self.options:
            print(option)

    def draw(self, surface):
        # Fill area for visibility
        surface.fill((100, 100, 100))

        # Display the options as text
        text_color = (0, 0, 0)  # Set the text color to black
        text_y = 15  # Starting y-coordinate for text

        # Draw header text adjusted to subsurface
        header_text = self.header_font.render("-- PLAYER OPTIONS --", True, text_color)
        header_rect = header_text.get_rect()
        header_rect.center = (surface.get_width() // 2, text_y)
        surface.blit(header_text, header_rect)
        text_y += 100  # Increase y-coordinate to draw options text

        # Draw player options adjusted to subsurface
        for option in self.options:
            text = self.option_font.render(option, True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (surface.get_width() // 2, text_y)
            surface.blit(text, text_rect)
            text_y += 50  # Increase y-coordinate for the next option

class GameBoard:
    def __init__(self, gameUI):
        #self.positions = positions
        self.gameUI = gameUI
        self.header_font = pygame.font.Font('freesansbold.ttf', 28)

        # Image attributes
        self.original_image = pygame.image.load("Gameboard.png")
        self.img_width = self.gameUI.screen_width // 2

    def update_position(self, character, position):
        self.positions[character] = position

    def display(self):
        print("Game Board:")
        for character, position in self.positions.items():
            print(f"{character} is at {position}")

    def draw(self, surface):
        # Draw the game board on the surface
        surface.fill((255, 255, 255))

        # Render header
        header_text = self.header_font.render("-- GAMEBOARD --", True, (0, 0, 0))
        header_rect = header_text.get_rect()
        header_rect.center = (surface.get_width() // 2, 15)
        surface.blit(header_text, header_rect)

        # Resize game board image using remaining rect height space
        gameboard_height = surface.get_height() - (header_rect.bottom + 5)
        scaled_image = pygame.transform.scale(self.original_image, (self.img_width, gameboard_height))

        # Draw the game board image
        surface.blit(scaled_image, (0, header_rect.bottom + 5))

class chatDisplay:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 250, 100
        self.chat_color = (255, 255, 245)
        self.text_color = (0, 0, 0)
        self.header_font = pygame.font.Font('freesansbold.ttf', 28)
        self.log_font = pygame.font.Font('freesansbold.ttf', 15)
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

        # Render the header
        header_text = self.header_font.render("-- CHAT LOG --", True, self.text_color)
        header_rect = header_text.get_rect()
        header_rect.center = (self.rect.x + self.rect.width // 2, self.rect.y + 15)
        self.screen.blit(header_text, header_rect)

        # Starting text location
        text_y = header_rect.bottom + 20

        # Render log messages
        for index, msg in enumerate(self.messages):
            chat_surface = self.log_font.render(msg, True, self.text_color)

            # Calculate text coordinates
            text_x = self.rect.x + 10
            self.screen.blit(chat_surface, (text_x, text_y))
            text_y += chat_surface.get_height() + 10 + (index * 30)


# class Text():
#     def __init__(self, screen, msg, x, y):

#             font = pygame.font.Font('freesansbold.ttf', 32)
#             text = font.render("Welcome! Please select a character:", True, (255,255,255), (0,0,0))
#             textRect = text.get_rect()
#             textRect.center = (gameUI.screen_width // 2, gameUI.screen_height // 2)
#             screen.blit(text, textRect)