from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
#import pygame

class Player:
    def __init__(self, character, location, is_connected, id, start = True, moved = False, cards=None, in_room=False, in_corner_room=False):
        self.id = id
        self.character = character
        self.location = location
        self.cards = cards
        self.is_connected = is_connected
        self.in_room = in_room
        self.in_corner_room = in_corner_room

    def get_location(self):
        return self.location
    def get_character(self):
        return self.character
    def get_id(self):
        return self.id
    def get_cards(self):
        return self.cards
    def get_is_connected(self):
        return self.is_connected
    def get_in_room(self):
        return self.in_room
    def get_in_corner_room(self):
        return self.in_corner_room
    
    def set_location(self, x):
        self.location = x
    def set_character(self, x):
        self.character = x
    def set_id(self, x):
        self.id = x
    def set_moved(self, x):
        self.moved = x
    def set_cards(self, x):
        self.cards = x
    def set_is_connected(self, x):
        self.is_connected = x
    def set_in_room(self, x):
        self.in_room = x
    def set_in_corner_room(self, x):
        self.in_corner_room = x

    #def __str__(self):
     #   return str(self.name)