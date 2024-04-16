from os import environ
from collections import deque
from typing import Dict
import pygame
import sys

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


class UI:
    """A class to represent the user-interface settings of the client."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)


class Button:
    def __init__(self, screen, msg, x, y, command_function: str) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.msg = msg
        self.command_function = command_function
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
    def __init__(self, gameUI, options, screen):
        self.gameUI = gameUI
        self.header_font = pygame.font.Font('freesansbold.ttf', 28)
        self.option_font = pygame.font.Font('freesansbold.ttf', 25)
        self.screen = screen
        self.game_controls = options
        self.header_x = None
        self.header_y = None

    def display(self):
        print("Options:")
        for option in self.options:
            print(option)

    # draws playeroptions
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
        self.header_x = surface.get_width() // 2
        self.header_y = text_y

        # running = True
        # while running:
        #     # took this block from main, needs editing. I just put it in 
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             print("Quit event detected")  # Debug print
        #             running = False
        #             pygame.quit()
        #             sys.exit()

        #         elif event.type == pygame.MOUSEBUTTONDOWN:
        #             mouse_x, mouse_y = pygame.mouse.get_pos()

        #             if move1.check_button(mouse_x, mouse_y):
        
        #                 return_value = move1.msg
                    
        #                 # this might need to move
        #                 running = False
                        
        #                 return(return_value)
                        
                     
        #             elif move2.check_button(mouse_x, mouse_y):

        #                 # in the future, will need additional if statements
                        
        #                 return_value = move1.msg
                    
        #                 # this might need to move
        #                 running = False
                        
        #                 return(return_value)
                   
                       
        #             elif move3.check_button(mouse_x, mouse_y):
                      
        #                 if m[2] == "Move To Hallway":
        #                     # keys = self.game_controls.cards.getKeys()
        #                     # cards = [ self.game_controls.cards[key] for key in keys]

        #                     display_options = o.get("Hallways")
                        
        #                 elif m[2] == "Move To Room and Suggest":

        #                     display_locations = o.get("Rooms")
        #                     display_suspects = self.game_controls.cards.get("suspect")
        #                     display_weapons = self.game_controls.cards.get("weapon")

        #                 elif m[2] == "Take Secret Passageway and Suggest":

        #                     display_locations = o.get("Rooms_Passageway")
        #                     display_suspects = self.game_controls.cards.get("suspect")
        #                     display_weapons = self.game_controls.cards.get("weapon")

        #                 running = False
                       

        #             # call the function that clears the screen and plots the next set of options based on what the user selected. 
        #             # cards is the paramter that gets updated depending on the previous option. 
        #             option_buttons(self.screen, surface, cards)

        #     pygame.display.update()

        #     # I'm hoping that this resets the tile for new text
        #     surface.fill((100, 100, 100))
        #     text_color = (0, 0, 0)  # Set the text color to black
        #     text_y = 15  # Starting y-coordinate for text

        #     self.all_location_buttons =[]

        #     # this should loop through locations and make a list of buttons
        #     for location in display_locations:
        #         new_button = Button(self.screen, location, surface.get_width() // 2, text_y)
        #         text_y = text_y + 50
        #         self.all_location_buttons.append(new_button)

        #     if len(display_suspects) != 0:

        #         self.all_suspect_buttons = []
        #         for suspects in display_suspects:
        #             new_button = Button(self.screen, suspects, surface.get_width() // 2, text_y)
        #             text_y = text_y + 50
        #             self.all_suspect_buttons.append(new_button)

        #     if len(display_weapons) != 0:

        #         self.all_weapon_buttons = []
        #         for weapons in display_weapons:
        #             new_button = Button(self.screen, weapons, surface.get_width() // 2, text_y)
        #             text_y = text_y + 50
        #             self.all_weapon_buttons.append(new_button)
        
        # running = True
        # while running:
    
        #     for weapons_button in self.all_weapon_buttons:
        #             weapons_button.draw_button()
            
        #     for suspects_button in self.all_suspect_buttons:
        #         suspects_button.draw_button()

        #     for location_button in self.all_location_buttons:
        #         location_button.draw_button()

        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         mouse_x, mouse_y = pygame.mouse.get_pos()
        #         for weapons_button in self.all_weapon_buttons:
        #             if weapons_button.check_button(mouse_x, mouse_y):
                        
        #                 print("weapons selection made")  # Debug print
        #                 weapon = weapons_button.msg

        #         for suspects_button in self.all_suspect_buttons:     
        #             if suspects_button.check_button(mouse_x, mouse_y):

        #                 print("suspect selection made")  # Debug print
        #                 suspect = suspects_button.msg

        #         for location_button in self.all_location_buttons:
        #             if location_button.check_button(mouse_x, mouse_y):
                        
        #                 print("location selection made")  # Debug print
        #                 location = location_button.msg
                        
        #     running = False
        #     pygame.display.update()


        # # Draw player options adjusted to subsurface
        # for option in self.options:
        #     text = self.option_font.render(option, True, text_color)
        #     text_rect = text.get_rect()
        #     text_rect.center = (surface.get_width() // 2, text_y)
        #     surface.blit(text, text_rect)
        #     text_y += 50  # Increase y-coordinate for the next option
        
        # def option_buttons(self, screen, surface, cards):

        #     # need to pass screen in. cards is meant to be the otions in game control relative to the choice made. May have to hardcode. 

        #     self.next_move_buttons = []
        #     for card in cards:
        #         new_button = Button(screen, card, surface.get_width() // 2, text_y)
                
        #         # need to change where each new button gets drawn
        #         text_y = text_y + 50
        #         self.next_move_buttons.append(new_button)

        #     running = True
        #     while running:
        
        #         for button in self.next_move_buttons:
        #             button.draw_button()

        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             print("Quit event detected")  # Debug print
        #             running = False
        #             pygame.quit()
        #             sys.exit()

        #         elif event.type == pygame.MOUSEBUTTONDOWN:
        #             mouse_x, mouse_y = pygame.mouse.get_pos()
        #             for button in self.next_move_buttons:
        #                 if button.check_button(mouse_x, mouse_y):
        #                     #self.s.send(f"Select_move:{button.msg}".encode())
        #                     print("move/suggest/accuse selected")  # Debug print

        #                     # send selected move back to game controller for state changes
        #                     selected_move = button.msg
        #                     running = False


        #     pygame.display.update()



        # # Draw player options adjusted to subsurface
        # for option in self.options:
        #     text = self.option_font.render(option, True, text_color)
        #     text_rect = text.get_rect()
        #     text_rect.center = (surface.get_width() // 2, text_y)
        #     surface.blit(text, text_rect)
        #     text_y += 50  # Increase y-coordinate for the next option
        # Draw player options adjusted to subsurface
        # for option in self.options:
        #     text = self.option_font.render(option, True, text_color)
        #     text_rect = text.get_rect()
        #     text_rect.center = (surface.get_width() // 2, text_y)
        #     surface.blit(text, text_rect)
        #     text_y += 50  # Increase y-coordinate for the next option

class GameBoard:
    def __init__(self, gameUI, current_locations: Dict):
        
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

    def draw(self, surface, position):
        # Draw the icon on the screen at the given position
        surface.blit(self.surface, position)

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
