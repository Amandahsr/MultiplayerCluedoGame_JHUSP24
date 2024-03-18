import sys
from UI import UI
from UI import Button
from player import Player
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import socket

class Client:
    def __init__(self):
        pygame.init()
        gameUI = UI()
        screen = pygame.display.set_mode((gameUI.screen_width, gameUI.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("ClueLess")
        # background = pygame.image.load("boardgame.webp")

        server = "localhost"
        port = 5555
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((server, port))
        except:
            pass

        user_text = ''
        while True:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render("Welcome! What is your name?", True, (255,255,255), (0,0,0))
            textRect = text.get_rect()
            textRect.center = (gameUI.screen_width // 2, gameUI.screen_height // 2)
            screen.blit(text, textRect)

            ms_button = Button(screen, "Miss Scarlet", 600, 500)
            ms_button.draw_button()

            pp_button = Button(screen, "Professor Plum", 600, 550)
            pp_button.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    user_text += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if(ms_button.check_button(mouse_x, mouse_y)):
                        s.send(ms_button.get_msg().encode())
                    if(pp_button.check_button(mouse_x, mouse_y)):
                        s.send(pp_button.get_msg().encode())

            # screen.fill((0,0,0))

            pygame.display.flip()

def main():
    C = Client()

if __name__ == "__main__":
    main()