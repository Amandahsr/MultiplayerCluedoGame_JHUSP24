import sys
import socket
from _thread import *

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn, client_list):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)
                if (reply not in client_list):
                    client_list += reply + ','
                #print(client_list)

            print('REPLY: ', reply)
            conn.sendall(str.encode(client_list))
            print(client_list)
        except Exception as error:
            print(error)
            break

    print("Lost connection")
    conn.close()

while True:
    global client_list
    client_list = ""

    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, client_list))
    
'''
class Server:
    game_board = {
        "Study_Room": [],
        "SH_Hall": [],
        "Hall_Room": [],
        "HL_Hall": [],
        "Lounge_Room": [],
        "SL_Hall": [],
        "Library_Room": [],
        "LB_Hall": [],
        "Billiard_Room": [],
        "BD_Hall": [],
        "Dining_Room": [],
        "LC_Hall": [],
        "Conservatory_Room": [],
        "CB_Hall": [],
        "Ball_Room": [],
        "BK_Hall": [],
        "Kitchen_Room": []
    }

    def __init__(self):
        ProfPlum = Player('Prof. Plum')
        self.game_board['SL_Hall'] = [str(ProfPlum)]
        
        MrsPeacock = Player('Mrs. Peacock')
        self.game_board['LC_Hall'] = [str(MrsPeacock)]

        MrGreen = Player('Mr. Green')
        self.game_board['CB_Hall'] = [str(MrGreen)]

        MrsWhite = Player('Mrs. White')
        self.game_board['BK_Hall'] = [str(MrsWhite)]

        ColMustard = Player('Col. Mustard')
        self.game_board['LD_Hall'] = [str(ColMustard)]

        MissScarlet = Player('Miss Scarlet')
        self.game_board['HL_Hall'] = [str(MissScarlet)]
        
        print(self.game_board)
'''