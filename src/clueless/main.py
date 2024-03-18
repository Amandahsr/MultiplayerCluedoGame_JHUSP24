import sys
from UI import UI
from UI import Button
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
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
        except Exception as e:
            print("Failed to connect to server:", e)
            sys.exit()

        self.main_menu()

    def main_menu(self):
        # Display the main menu UI
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Welcome! Please select a character:", True, (255,255,255), (0,0,0))
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
            self.screen.fill((0,0,0))
            self.screen.blit(text, textRect)
            for button in buttons:
                button.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.check_button(mouse_x, mouse_y):
                            self.s.send(f"select_character:{button.msg}".encode())
                            running = False
                            self.lobby()

            pygame.display.update()

    def lobby(self):
        # Display the lobby UI and update selected characters
        running = True
        while running:
            self.screen.fill((0,0,0))
            try:
                data = self.s.recv(1024).decode("utf-8")
                if data.startswith("lobby_update:"):
                    selected_characters = data.split(":")[1].split(",")
                    y_pos = 100
                    for character in selected_characters:
                        text = pygame.font.Font('freesansbold.ttf', 20).render(character, True, (255,255,255), (0,0,0))
                        self.screen.blit(text, (100, y_pos))
                        y_pos += 30
            except Exception as e:
                print("Failed to receive data from server:", e)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    client = Client()