from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
#import pygame
from player import Player
#import server
import random

class GameController:

    def __init__(self, state):
        self.state = state
        self.cards = {'suspect': ['Professor Plum', 'Mrs. Peacock', 'Mr. Green', 'Mrs. White', 'Col. Mustard', 'Miss Scarlet'], 
             'room': ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen'],
             'weapon': ['candlestick', 'wrench', 'knife', 'revolver', 'rope', 'lead pipe']}
        self.available_cards = ['Professor Plum', 'Mrs. Peacock', 'Mr. Green', 'Mrs. White', 'Col. Mustard', 'Miss Scarlet', 'Study', 
                                'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen', 
                                'candlestick', 'wrench', 'knife', 'revolver', 'rope', 'lead pipe']
        
    def set_available_cards(self, x):
        self.available_cards = x
    
    def create_answer(self):
        suspect = random.choice(self.cards.get('suspect'))
        room = random.choice(self.cards.get('room'))
        weapon = random.choice(self.cards.get('weapon'))
        answer = {'suspect': suspect, 'room': room, 'weapon': weapon}
        self.available_cards.remove(suspect)
        self.available_cards.remove(room)
        self.available_cards.remove(weapon)
        return answer

    def initialize_cards(): #is there a minimum # of players
        cards = {}

    def initialize_player(self, character): #need character from Server i think, order of players joining as well
        if character == 'Professor Plum':
            p = Player.__init__(1, 'Professor Plum', 'SL_Hall', initialize_cards(), True)
        if character == 'Mrs. Peacock':
            p = Player.__init__(2, 'Mrs. Peacock', 'LC_Hall', initialize_cards(), True)
        if character == 'Mr. Green':
            p = Player.__init__(3, 'Mr. Green', 'CB_Hall', initialize_cards(), True)
        if character == 'Mrs. White':
            p = Player.__init__(4, 'Mrs. White', 'BK_Hall', initialize_cards(), True)
        if character == 'Col. Mustard':
            p = Player.__init__(5, 'Col. Mustard', 'LD_Hall', initialize_cards(), True)
        if character == 'Miss Scarlet':
            Player.set_id(6)
            p = Player.__init__(6, 'Miss Scarlet', 'HL_Hall', initialize_cards(), True)
        return p

    def valid_moves():
        return moves

g = GameController([])
print(g.create_answer())