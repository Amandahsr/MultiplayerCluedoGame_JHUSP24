from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

class Player:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)