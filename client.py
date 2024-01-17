from tabulate import tabulate
import random
import os
from network import Network
import pickle
import time
import socket

board_len = 10
playe_board = [["" for i in range(board_len)] for x in range(board_len)]
opponent_board = [["" for i in range(board_len)] for x in range(board_len)]

# Function for creating a table
def create_table(board_len,data):
    
    # Table to print the players board
    header = [chr(65+i) for i in range(board_len)]
    board_index = range(1,board_len+1)
    table = tabulate(data,tablefmt="rounded_grid",showindex=board_index,headers=header)
    return table

# Function for asking a user input
def ask_user_input(board_len, message,board,com_board):
    print(tabulate([[create_table(board_len,board), create_table(board_len,com_board)]], rowalign="center", tablefmt="grid"))
    user_input = input(message).strip()
    while not(int(user_input[1:])-1 < board_len and ord(user_input[0].upper())-65 < board_len):
        user_input = input("Incorrect Coordinate!! Please type in your coordinate like H7: ").strip()
    return [int(user_input[1:])-1,ord(user_input[0].upper())-65]

# Function for placing ships
def place_ships(com_board,board_len,board):

    for i in range(2,6):

        pos_ok = False
        while not pos_ok:
            os.system("clear")
            pos = ask_user_input(board_len,f"You should now place a Ship with a size of {i}. Please choose the starting pos of the ship: ",board,com_board)
            orientation = input("vertical(v) or horizontal(h)?: ")
            while orientation.lower() != "v" and orientation.lower() != "h":
                orientation = input("Invalid argument. vertical(v) or horizontal(h)?: ")
            if (pos[0]+i) % board_len == 1 or (pos[1]+i) % board_len == 1:
                continue
            if orientation == "h":
                temp_status = False
                for x in range(i):
                    if pos[1]+x >= board_len:
                        temp_status = False
                        break
                    if com_board[pos[0]][pos[1]+x] == "":
                        temp_status = True
                    else:
                        temp_status = False
                        break
                if temp_status == False:
                    continue
                else:
                    pos_ok = True
                    for x in range(i):
                        com_board[pos[0]][pos[1]+x] = f"{i}"
            else:
                temp_status = False
                for x in range(i):
                    
                    if pos[0]+x >= board_len:
                        temp_status = not temp_status
                        break
                    if com_board[pos[0]+x][pos[1]] == "":
                        temp_status = True
                    else:
                        temp_status = False
                        break
                if temp_status == False:
                    continue
                else:
                    pos_ok = True
                    for x in range(i):
                        com_board[pos[0]+x][pos[1]] = f"{i}"
    return com_board




def main():
    n = Network()
    player = int(n.getP())

    os.system("clear")
    print(f"=============================Welcome to the Python Battleship Game=============================\n\nYou are player {player}.\n\n")
    print("Please choose your ships for the board:")
    time.sleep(2)

    player_board = place_ships(opponent_board,board_len,playe_board)
    
    run = True
    game = n.send(("play",player_board))
    while run:
        try:
            if not n.send("bothwent"):
                print("Waiting for the Player.......")
                os.system("clear")
            else:
                if 4 in (sun := n.send("sunkships")):
                    print(f"Game Over! Player {sun.index(4)+1} Won")
                if (now_turn := n.send("turn")) == player:
                    os.system("clear")
                    print(f"It's your turn! You are player {player}")
                    time.sleep(2)
                    os.system("clear")
                    moves = n.send("getplayerboards")
                    ui = ask_user_input(board_len,"Please type in your coordinate like H7: ",moves[player],[["" if type(moves[(player+1)%2][x][value]) == int else moves[(player+1)%2][x][value] for value in range(board_len)] for x in range(board_len)])
                    # try:
                    #     print(n.send(ui))
                    #     time.sleep(2)
                    # except Exception as e:
                    #     print("Error catched",e)
                    #     time.sleep(2)
                    while n.send(("check",ui)) == "-X":
                        os.system("clear")
                        print("You already guessed this coordinate")
                        ui = ask_user_input(board_len,"Please type in your coordinate like H7: ",moves[player],[["" if type(moves[(player+1)%2][x][value]) == int else moves[(player+1)%2][x][value] for value in range(board_len)] for x in range(board_len)])
                    if (result := n.send(ui)) == "S" or result == "H":
                        os.system("clear")
                        print(f"{chr(65+ui[1])}{ui[0]+1} is a Hit\n")
                        if result == "S":
                            print("Sunk")
                        time.sleep(2)
                    else:
                        os.system("clear")
                        print(f"{chr(65+ui[1])}{ui[0]+1} is a Miss\n")
                        time.sleep(2)
                    os.system("clear")
                    n.send("changeturn")
                    print("Is all okay?")
                else:
                    print(f"\n\n\n\nPlayer {(player+1)%2} is playing!\n\n\n\n")
                    time.sleep(4)
                if not n.send("connected"):
                    run = False
                

        except:
            run = False
            print("Couldn't get game")
            break

while True:
    main()