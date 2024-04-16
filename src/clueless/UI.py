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
    def __init__(self, gameUI, game_controls, screen):
        self.options = options
        self.gameUI = gameUI
        self.header_font = pygame.font.Font('freesansbold.ttf', 28)
        self.option_font = pygame.font.Font('freesansbold.ttf', 25)
        self.screen = screen
        self.game_controls = game_controls

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
        text_y += 30  # Increase y-coordinate to draw options text

        # m is moves, o in options
        m,o = self.game_controls.valid_moves()
        

        # update to be more dynamic, 5 options 

        # pass
        move1 = Button(self.screen, m[0], surface.get_width() // 2, text_y )
        text_y = text_y + 50
        # accuse
        move2 = Button(self.screen, m[1], surface.get_width() // 2, text_y)
        text_y = text_y + 50
        #move/suggest
        move3 = Button(self.screen, m[2], surface.get_width() // 2, text_y)

        running = True
        while running:
            move1.draw_button()
            move2.draw_button()
            move3.draw_button()
            
            # took this block from main, needs editing. I just put it in 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if move1.check_button(mouse_x, mouse_y):
        
                        return_value = move1.msg
                    
                        # this might need to move
                        running = False
                        
                        return(return_value)
                        
                     
                    elif move2.check_button(mouse_x, mouse_y):

                        # in the future, will need additional if statements
                        
                        return_value = move1.msg
                    
                        # this might need to move
                        running = False
                        
                        return(return_value)
                   
                       
                    elif move3.check_button(mouse_x, mouse_y):
                      
                        if m[2] == "Move To Hallway":
                            # keys = self.game_controls.cards.getKeys()
                            # cards = [ self.game_controls.cards[key] for key in keys]

                            display_options = o.get("Hallways")
                        
                        elif m[2] == "Move To Room and Suggest":

                            display_locations = o.get("Rooms")
                            display_suspects = self.game_controls.cards.get("suspect")
                            display_weapons = self.game_controls.cards.get("weapon")

                        elif m[2] == "Take Secret Passageway and Suggest":

                            display_locations = o.get("Rooms_Passageway")
                            display_suspects = self.game_controls.cards.get("suspect")
                            display_weapons = self.game_controls.cards.get("weapon")

                        running = False
                       

                    # call the function that clears the screen and plots the next set of options based on what the user selected. 
                    # cards is the paramter that gets updated depending on the previous option. 
                    option_buttons(self.screen, surface, cards)

            pygame.display.update()

            # I'm hoping that this resets the tile for new text
            surface.fill((100, 100, 100))
            text_color = (0, 0, 0)  # Set the text color to black
            text_y = 15  # Starting y-coordinate for text

            self.all_location_buttons =[]

            # this should loop through locations and make a list of buttons
            for location in display_locations:
                new_button = Button(self.screen, location, surface.get_width() // 2, text_y)
                text_y = text_y + 50
                self.all_location_buttons.append(new_button)

            if len(display_suspects) != 0:

                self.all_suspect_buttons = []
                for suspects in display_suspects:
                    new_button = Button(self.screen, suspects, surface.get_width() // 2, text_y)
                    text_y = text_y + 50
                    self.all_suspect_buttons.append(new_button)

            if len(display_weapons) != 0:

                self.all_weapon_buttons = []
                for weapons in display_weapons:
                    new_button = Button(self.screen, weapons, surface.get_width() // 2, text_y)
                    text_y = text_y + 50
                    self.all_weapon_buttons.append(new_button)

        running = True
        while running:
        
                for weapons_button in self.all_weapon_buttons:
                     weapons_button.draw_button()
                
                for suspects_button in self.all_suspect_buttons:
                    suspects_button.draw_button()

                for location_button in self.all_location_buttons:
                    location_button.draw_button()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for weapons_button in self.all_weapon_buttons:
                        if weapons_button.check_button(mouse_x, mouse_y):
                            
                            print("weapons selection made")  # Debug print
                            weapon = weapons_button.msg

                    for suspects_button in self.all_suspect_buttons:     
                        if suspects_button.check_button(mouse_x, mouse_y):

                            print("suspect selection made")  # Debug print
                            suspect = suspects_button.msg

                    for location_button in self.all_location_buttons:
                        if location_button.check_button(mouse_x, mouse_y):
                            
                            print("location selection made")  # Debug print
                            location = location_button.msg
                            
                running = False
    

            pygame.display.update()

            return(weapon, suspect, location)



        # # Draw player options adjusted to subsurface
        # for option in self.options:
        #     text = self.option_font.render(option, True, text_color)
        #     text_rect = text.get_rect()
        #     text_rect.center = (surface.get_width() // 2, text_y)
        #     surface.blit(text, text_rect)
        #     text_y += 50  # Increase y-coordinate for the next option
        
        def option_buttons(self, screen, surface, cards):

            # need to pass screen in. cards is meant to be the otions in game control relative to the choice made. May have to hardcode. 

            self.next_move_buttons = []
            for card in cards:
                new_button = Button(screen, card, surface.get_width() // 2, text_y)
                
                # need to change where each new button gets drawn
                text_y = text_y + 50
                self.next_move_buttons.append(new_button)

            running = True
            while running:
        
                for button in self.next_move_buttons:
                    button.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected")  # Debug print
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for button in self.next_move_buttons:
                        if button.check_button(mouse_x, mouse_y):
                            #self.s.send(f"Select_move:{button.msg}".encode())
                            print("move/suggest/accuse selected")  # Debug print

                            # send selected move back to game controller for state changes
                            selected_move = button.msg
                            running = False


            pygame.display.update()



        # # Draw player options adjusted to subsurface
        # for option in self.options:
        #     text = self.option_font.render(option, True, text_color)
        #     text_rect = text.get_rect()
        #     text_rect.center = (surface.get_width() // 2, text_y)
        #     surface.blit(text, text_rect)
        #     text_y += 50  # Increase y-coordinate for the next option
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
