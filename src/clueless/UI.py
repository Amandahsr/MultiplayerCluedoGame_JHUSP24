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
    def __init__(self, gameUI, current_locations):
        
        self.positions = current_locations # This will store the character positions
        self.gameUI = gameUI
        self.character_icons = {
            "Miss Scarlet": CharacterIcon((255, 0, 0), "MS"),
            "Col. Mustard": CharacterIcon((255, 255, 0), "CM"),
            "Mrs. White": CharacterIcon((128, 128, 128), "MW"),
            "Mr. Green": CharacterIcon((0, 255, 0), "MG"),
            "Mrs. Peacock": CharacterIcon((0, 255, 255), "MP"),
            "Professor Plum": CharacterIcon((128, 0, 128), "PP")
        }
        #self.load_icons()
        
        # Load the game board image
        original_image = pygame.image.load("Gameboard.png") 
        # Set the image dimensions to fit the game board section of the display
        img_width = self.gameUI.screen_width // 2
        img_height = self.gameUI.screen_height // 2
        self.image = pygame.transform.scale(original_image, (img_width, img_height))

    def update_position(self, character, position):
        self.positions[character] = position

    def display(self):
        for character, position in self.positions.items():
            if position in board_spots:
                #print(f"{character} is at {position}")
                spot_coordinates = board_spots[position]
                character_icon = self.character_icons[character]
                character_icon.draw(surface, spot_coordinates)
            pass

    def draw(self, surface):
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
            "Ballroom": (center_x -5, center_y + 130),
            "BK_Hall": (center_x + 95, center_y + 135),
            "Kitchen": (center_x + 200, center_y + 130)
        }
        
        # Iterate over all characters and their positions to draw them
        for character, position in self.positions.items():
            # Get the board location for the character's position
            board_location = board_spots.get(position)
            if board_location:
                icon = self.character_icons.get(character)
                if icon:
                    # Adjust the coordinates to make them the center of the icon
                    icon_width = icon.radius * 2
                    icon_height = icon.radius * 2
                    icon_x = board_location[0] - icon_width / 2
                    icon_y = board_location[1] - icon_height / 2
                    adjusted_location = (icon_x, icon_y)
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

    def draw(self, screen, position):
        # Draw the icon on the screen at the given position
        screen.blit(self.surface, position)

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
