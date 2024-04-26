import os
from os import environ
from typing import Dict, List
import pygame
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


class UI:
    """A class to represent the user-interface settings of the client."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)


class Button:
    def __init__(self, screen, button_color, msg, x, y, command_function: str, text_color=None) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 150, 50
        self.button_color = button_color
        self.font = pygame.font.SysFont(None, 30)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.msg = msg
        self.command_function = command_function

        # Determine text_color
        if not text_color:
            self.text_color = (255, 255, 255)
        else:
            self.text_color = text_color

        self.prep_msg(msg)

    def get_msg(self):
        return self.msg

    def prep_msg(self, msg):
        #print(f"msg: {msg}, text_color: {self.text_color}, button_color: {self.button_color}")
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
        self.header_font = pygame.font.Font("freesansbold.ttf", 28)
        self.card_font = pygame.font.Font("freesansbold.ttf", 20)
        self.screen_color = (255, 255, 245)
        self.text_color = (0, 0, 0)

    def display(self):
        print(f"Character: {self.character_name}")
        print("Cards: " + ", ".join(self.cards))

    def draw(self, surface):
        # Draw the player card on the surface
        surface.fill(self.screen_color)

        # Render header
        header_text = self.header_font.render(f"-- {self.character_name} CARDS --", True, self.text_color)
        header_rect = header_text.get_rect()
        header_rect.center = (surface.get_width() // 2, 15)
        surface.blit(header_text, header_rect)

        # Starting text location
        text_y = header_rect.bottom + 20

        # Render player cards text
        for card in self.cards:
            text = self.card_font.render(card, True, self.text_color)
            text_rect = text.get_rect()
            text_rect.center = (surface.get_width() // 2, text_y)
            surface.blit(text, text_rect)
            text_y += 30


class PlayerOptions:
    def __init__(self, gameUI, options, screen):
        self.gameUI = gameUI
        self.header_font = pygame.font.Font("freesansbold.ttf", 28)
        self.option_font = pygame.font.Font("freesansbold.ttf", 25)
        self.screen = screen
        self.game_controls = options
        self.screen_color = (255, 255, 255)
        self.header_x = None
        self.header_y = None

    def display(self):
        print("Options:")
        for option in self.options:
            print(option)

    # draws playeroptions
    def draw(self, surface):
        # Fill area for visibility
        surface.fill(self.screen_color)

        # Display the options as text
        text_color = (0, 0, 0)
        text_y = 15

        # Draw header text adjusted to subsurface
        header_text = self.header_font.render("-- PLAYER OPTIONS --", True, text_color)
        header_rect = header_text.get_rect()
        header_rect.center = (surface.get_width() // 2, text_y)
        surface.blit(header_text, header_rect)
        self.header_x = surface.get_width() // 2
        self.header_y = text_y


class GameBoard:
    def __init__(self, gameUI, current_locations: Dict):

        self.positions = current_locations  # This will store the character positions
        self.gameUI = gameUI
        self.character_icons = {
            "Miss Scarlet": CharacterIcon((255, 0, 0), "MS"),
            "Col. Mustard": CharacterIcon((255, 255, 0), "CM"),
            "Mrs. White": CharacterIcon((128, 128, 128), "MW"),
            "Mr. Green": CharacterIcon((0, 255, 0), "MG"),
            "Mrs. Peacock": CharacterIcon((0, 255, 255), "MP"),
            "Professor Plum": CharacterIcon((128, 0, 128), "PP"),
        }
        # self.load_icons()

        # Load the game board image
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        gameboard_img_path = os.path.join(ROOT_DIR, 'Gameboard.png')
        original_image = pygame.image.load(gameboard_img_path)
        
        # Set the image dimensions to fit the game board section of the display
        img_width = self.gameUI.screen_width // 2
        img_height = self.gameUI.screen_height // 2
        self.image = pygame.transform.scale(original_image, (img_width, img_height))

    def update_position(self, character, position):
        self.positions[character] = position


    def display(self):
        for character, position in self.positions.items():
            if position in board_spots:
                # print(f"{character} is at {position}")
                spot_coordinates = board_spots[position]
                character_icon = self.character_icons[character]
                character_icon.draw(surface, spot_coordinates)
            pass

    def draw(self, surface, locations: None):
        surface.blit(self.image, (0, 0))  # Blit the game board image

        # Calculate the center of the image
        center_x = self.image.get_width() // 2
        center_y = self.image.get_height() // 2

        # Map each board spot to its corresponding coordinates
        board_spots = {
            "Study": (center_x - 210, center_y - 125),
            "SH_Hall": (center_x - 110, center_y - 135),
            "Hall": (center_x - 5, center_y - 125),
            "HL_Hall": (center_x + 95, center_y - 135),
            "Lounge": (center_x + 200, center_y - 125),
            "SL_Hall": (center_x - 210, center_y - 70),
            "HB_Hall": (center_x - 5, center_y - 70),
            "LD_Hall": (center_x + 200, center_y - 70),
            "Library": (center_x - 210, center_y + 10),
            "LB_Hall": (center_x - 110, center_y - 3),
            "Billiard": (center_x - 5, center_y + 10),
            "BD_Hall": (center_x + 95, center_y - 3),
            "Dining": (center_x + 200, center_y + 10),
            "LC_Hall": (center_x - 210, center_y + 70),
            "BB_Hall": (center_x - 5, center_y + 70),
            "DK_Hall": (center_x + 200, center_y + 70),
            "Conservatory": (center_x - 210, center_y + 130),
            "CB_Hall": (center_x - 110, center_y + 135),
            "Ballroom": (center_x - 5, center_y + 130),
            "BK_Hall": (center_x + 95, center_y + 135),
            "Kitchen": (center_x + 200, center_y + 130),
            "MS_Start": (center_x + 95, center_y - 170),
            "CM_Start": (center_x + 245, center_y - 70),
            "MW_Start": (center_x + 95, center_y + 170),
            "MG_Start": (center_x - 110, center_y + 170),
            "MP_Start": (center_x - 250, center_y + 70),
            "PP_Start": (center_x - 250, center_y - 70),
        }

        # Iterate over all characters and their positions to draw them
        for character, position in self.positions.items():
            # Get the board location for the character's position
            board_location = board_spots.get(position)
            icon = self.character_icons.get(character)
            icon_width = icon.radius * 2
            icon_height = icon.radius * 2
            icon_x = board_location[0] - icon_width / 2
            icon_y = board_location[1] - icon_height / 2
            adjusted_location = (icon_x, icon_y)

            print(f"{character} is at {position}")
            # Draw the character icon at the pixel coordinates
            icon.draw(surface, adjusted_location)



class CharacterIcon:
    def __init__(self, color, initials, radius=17):
        self.color = color
        self.initials = initials
        self.radius = radius

        # Create a surface for the icon
        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        # Draw the circle on the surface
        pygame.draw.circle(self.surface, color, (radius, radius), radius)

        # Create a font object
        font = pygame.font.Font(None, 24)  # You can adjust the size as needed

        # Render the initials
        text = font.render(initials, True, (0, 0, 0))  # Black text

        # Get the width and height of the text
        text_width, text_height = text.get_size()

        # Calculate the position of the text
        text_x = radius - text_width // 2
        text_y = radius - text_height // 2

        # Draw the text on the surface
        self.surface.blit(text, (text_x, text_y))

    def draw(self, surface, position):
        # Draw the icon on the screen at the given position
        print(f"position passed to icon.draw: {position}")
        surface.blit(self.surface, position)


class chatDisplay:
    def __init__(self, rect, screen, x, y, log_msgs: List[str]):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 250, 100
        self.chat_color = (255, 255, 245)
        self.text_color = (0, 0, 0)
        self.header_font = pygame.font.Font("freesansbold.ttf", 28)
        self.log_font = pygame.font.Font("freesansbold.ttf", 15)
        self.rect = rect
        self.rect.center = (x, y)
        self.log_msgs = log_msgs

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
        for _, msg in enumerate(self.log_msgs):
            chat_surface = self.log_font.render(msg, True, self.text_color)

            # Calculate text coordinates
            text_x = self.rect.x + 10
            self.screen.blit(chat_surface, (text_x, text_y))
            text_y += 20


# class Text():
#     def __init__(self, screen, msg, x, y):

#             font = pygame.font.Font('freesansbold.ttf', 32)
#             text = font.render("Welcome! Please select a character:", True, (255,255,255), (0,0,0))
#             textRect = text.get_rect()
#             textRect.center = (gameUI.screen_width // 2, gameUI.screen_height // 2)
#             screen.blit(text, textRect)
