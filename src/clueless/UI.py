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
