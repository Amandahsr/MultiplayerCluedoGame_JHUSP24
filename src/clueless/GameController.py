from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
#import pygame
from player import Player
#import server
import random

class GameController:

    def __init__(self, players = []):
        self.cards = {'suspect': ['Professor Plum', 'Mrs. Peacock', 'Mr. Green', 'Mrs. White', 'Col. Mustard', 'Miss Scarlet'], 
             'room': ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen'],
             'weapon': ['candlestick', 'wrench', 'knife', 'revolver', 'rope', 'lead pipe']}
        self.available_cards = ['Professor Plum', 'Mrs. Peacock', 'Mr. Green', 'Mrs. White', 'Col. Mustard', 'Miss Scarlet', 'Study', 
                                'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen', 
                                'candlestick', 'wrench', 'knife', 'revolver', 'rope', 'lead pipe']
        self.players = players
        self.current_player = "" #need to figure out how to initialize this for a variable number of players
        self.board = {"Study": ["SL_Hall", "SH_Hall"], "Hall" : ["SH_Hall", "HB_Hall", "HL_Hall"],
                      "Lounge" : ["HL_Hall", "LD_Hall"], "Library": ["SL_Hall", "LB_Hall", "LC_Hall"],
                      "Billiard": ["HB_Hall", "LB_Hall", "BB_Hall", "BD_Hall"], "Dining" : ["LD_Hall", "BD_Hall", "DK_Hall"],
                      "Conservatory": ["LC_Hall", "CB_Hall"], "Ballroom" : ["CB_Hall", "BB_Hall", "BK_Hall"], 
                      "Kitchen": ["BK_Hall", "DK_Hall"]}
        self.rooms = ["Study", "Hall", "Lounge", "Library", "Billiard", "Dining", "Conversatory", "Ballroom", "Kitchen"]
        self.corner_rooms = ["Study", "Conservatory", "Lounge", "Kitchen"]
        self.hallways = ["SL_Hall", "SH_Hall", "HL_Hall", "HB_Hall", "LD_Hall", "LB_Hall", "BD_Hall", "LC_Hall","BB_Hall", "DK_Hall", "CB_Hall", "BK_Hall"]
        self.turn_order = []

    def set_available_cards(self, x):
        self.available_cards = x
    
    def create_answer(self): #must be called before initialize_players
        suspect = random.choice(self.cards.get('suspect'))
        room = random.choice(self.cards.get('room'))
        weapon = random.choice(self.cards.get('weapon'))
        answer = {'suspect': suspect, 'room': room, 'weapon': weapon}
        self.available_cards.remove(suspect)
        self.available_cards.remove(room)
        self.available_cards.remove(weapon)
        return answer

    def initialize_player(self, character): #need character from Server i think, order of players joining as well
        if character == 'Professor Plum':
            p = Player('Professor Plum', 'SL_Hall', True, 1)
        if character == 'Mrs. Peacock':
            p = Player('Mrs. Peacock', 'LC_Hall', True, 2)
        if character == 'Mr. Green':
            p = Player('Mr. Green', 'CB_Hall', True, 3)
        if character == 'Mrs. White':
            p = Player('Mrs. White', 'BK_Hall', True, 4)
        if character == 'Col. Mustard':
            p = Player('Col. Mustard', 'LD_Hall', True, 5)
        if character == 'Miss Scarlet':
            p = Player('Miss Scarlet', 'HL_Hall', True, 6)
        self.players.append(p) #adds players to game state
        return p
    
    def initialize_turns(self): #initializing the turn order
        for i in self.players:
            self.turn_order.append(i.id)
        self.turn_order.sort() #list of ordered player ids
        for i in self.players:
            if i.id == self.turn_order[0]:
                self.current_player = i

    def initialize_cards(self): #to be executed when all players have joined
        for i in self.players: #cards chosen randomly for each player
            cards = []
            for j in range(18//len(self.players)): #18 is the number of total available cards
                new_card = random.choice(self.available_cards)
                cards.append(new_card)
                self.available_cards.remove(new_card)
            i.set_cards(cards)
        if len(self.available_cards) != 0: #if there are 4 or 5 players, this will be the case
            for i in range(len(self.available_cards)): #assign the rest of the cards to players, resulting in an uneven distribution of cards
                new_card = random.choice(self.available_cards)
                self.players[i].get_cards().append(new_card)

    def valid_moves(self): #moves goes to player or client to display
        moves = [] #initializing the valid moves
        options = {"Hallways": None, "Rooms": None, "Rooms_Passageway": None} #initializes the options a player can move to
        moves.append("Pass") #every turn a player can pass
        moves.append("Accuse") #every turn a player can accuse

        #First turn logic
        if self.current_player.start == True: #first move must be to adjacent hallway
            moves.append("Move To Hallway")
            options["Hallways"] = self.current_player.location #player's location is initialized to starter hall
            self.current_player.start == False #it is not the current player's first move anymore, set to False
            return moves, options
        
        #Move to Room from Hallway
        if self.current_player.location in self.hallways:
            moves.append("Move To Room and Suggest")
            if self.current_player.location == "SL_Hall": #creating the rooms the player can move into
                options["Rooms"] = ["Study", "Library"]
            elif self.current_player.location == "SH_Hall":
                options["Rooms"] = ["Study", "Hall"]
            elif self.current_player.location == "HL_Hall":
                options["Rooms"] = ["Hall", "Lounge"]
            elif self.current_player.location == "HB_Hall":
                options["Rooms"] = ["Hall", "Billiard"]
            elif self.current_player.location == "LD_Hall":
                options["Rooms"] = ["Library", "Dining"]
            elif self.current_player.location == "LB_Hall":
                options["Rooms"] = ["Library", "Billiard"]
            elif self.current_player.location == "BD_Hall":
                options["Rooms"] = ["Billiard", "Dining"]
            elif self.current_player.location == "LC_Hall":
                options["Rooms"] = ["Library", "Conservatory"]
            elif self.current_player.location == "BB_Hall":
                options["Rooms"] = ["Billiard", "Ballroom"]
            elif self.current_player.location == "DK_Hall":
                options["Rooms"] = ["Dining", "Kitchen"]
            elif self.current_player.location == "CB_Hall":
                options["Rooms"] = ["Conservatory", "Ballroom"]
            elif self.current_player.location == "BK_Hall":
                options["Rooms"] = ["Ballroom", "Kitchen"]
            return moves, options

        #Move to hallway from room, take secret passageway, and stay in room (if moved) and suggest
        if self.current_player.in_room == True:
            num = 0
            adj_halls = self.board.get(self.current_player.location) #adjacent hallways
            max = len(adj_halls) #used to compare number of players in the adjacent halls
            for i in self.players: #check to see if hallways from the room are blocked
                if i.location in adj_halls: #looks up the hallways adjacent to room and checks against other player's locations
                    adj_halls.remove(i.location) #removes hall in player in hall because it is not valid to move to that hall
                    num += 1
                if num != max: #comparing the number of players in adjacent hallways to the number of adjacent hallways
                    moves.append("Move To Hallway")
                    options["Hallways"] = adj_halls
            if self.current_player.location in self.corner_rooms:
                moves.append("Take Secret Passageway and Suggest")
                if self.current_player.location == "Study":
                    options["Rooms_Passageway"] = "Kitchen"
                elif self.current_player.location == "Kitchen":
                    options["Rooms_Passageway"] = "Study"
                elif self.current_player.location == "Lounge":
                    options["Rooms_Passageway"] = "Conversatory"
                elif self.current_player.location == "Conversatory":
                    options["Rooms_Passageway"] = "Lounge"
            if self.current_player.moved == True: #if player was moved to a room by another player via suggestion
                moves.append("Suggest") #stay in room and suggest
            return moves, options
        
    #used by suggest function to determine who should disprove the suggestion next
    #used by execute move to reset current player, current is a player object
    def next_player(self, current): 
        current_id = current.id
        current_index = self.turn_order.index(current_id)
        if current_index == (len(self.turn_order)-1):
            next_player_id = self.turn_order[0]
        else:
            next_player_id = self.turn_order[current_index+1]
        for i in self.players:
            if i.id == next_player_id:
                next_player = i
        return next_player
    
    def disapprove_suggestion(self, suggestion): #need the suggestion from player selection, suggestion is assumed to be a dict
        disapproval = []
        next = self.next_player(cur)
        num = 0
        while num < (len(self.players)-1):
            if suggestion.get("suspect") in self.next_player(next).cards:
                disapproval.append(suggestion.get("suspect"))
            if suggestion.get("room") in self.next_player(next).cards:
                disapproval.append(suggestion.get("room"))
            if suggestion.get("weapon") in self.next_player(next).cards:
                disapproval.append(suggestion.get("weapon")) 
            if len(disapproval) != 0: #if player can disapprove suggestion, break loop
                break
            next = self.next_player(next)
            num += 1  
        return next, disapproval #returns player who disapproved and cards to disapprove, needs to go to another class
            

    #handles the suggestion logic after a player selected their move, called during execute_move
    def suggest(self, suggestion): #need the suggestion from player selection, suggestion is assumed to be a dict
        for i in self.players:
            if i.character == suggestion.get("suspect"):
                i.set_location(suggestion.get("location"))
                i.set_moved(True)
                break
        self.disapprove_suggestion(suggestion)
            
        
            

    #handles the accusation logic after a player selected their move, called during execute_move
    def accuse(self):
        #needs to be implemented
        return None
            
        #execute move needs the selected move and the option (i.e., which room, hallway, passageway player selected)
    def execute_move(self, move, option):
        if move == "Take Secret Passageway and Suggest": #game state updated
            self.current_player.set_location(option)
            self.current_player.set_in_room(True)
            self.current_player.in_corner_room(True)
            self.suggest()
        if move == "Move To Room and Suggest":
            self.current_player.set_location(option)
            self.current_player.set_in_room(True)
            if option in self.corner_rooms:
                self.current_player.set_in_corner_room(True)   
            else:
                self.current_player.set_in_corner_room(False)   
            self.suggest()
        if move == "Move To Hallway":
            self.current_player.set_location(option)
            self.current_player.set_in_room(False)
            self.current_player.set_in_corner_room(False)   
        if move == "Suggest":
            self.current_player.set_moved(False)
            self.current_player.set_in_room(True)
            if option in self.corner_rooms:
                self.current_player.set_in_corner_room(True)   
            else:
                self.current_player.set_in_corner_room(False)
        if move == "Accuse":
            self.accuse()
        #set next current player as the turn is complete, if "Pass" is chosen, current_player is reset as well
        self.current_player = self.next_player(self.current_player)
            
                    
        
        
g = GameController()
g.initialize_player('Professor Plum')
g.initialize_player('Mrs. Peacock')
g.initialize_player('Mr. Green')
g.initialize_player('Mrs. White')
g.initialize_player('Col. Mustard')
g.initialize_player('Miss Scarlet')
g.create_answer()
g.initialize_cards()
g.initialize_turns()

#for i in g.players:
 #   print(i.cards)
  #  print(i.character)