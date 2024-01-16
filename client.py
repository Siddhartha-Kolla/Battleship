from tabulate import tabulate
import random
import os
from network import Network
import pickle
import time

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
            orientation = input("vertical or horizontal?: ")
            while orientation.lower() != "vertical" and orientation.lower() != "horizontal":
                orientation = input("Invalid argument. vertical or horizontal?: ")
            if (pos[0]+i) % board_len == 1 or (pos[1]+i) % board_len == 1:
                continue
            if orientation == "horizontal":
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
    game = n.send("get")
    game.Went[player] = True
    game.moves[player] = player_board
    game = n.send("play")
    while run:
        try:
            game = n.send("get")         
            if not game.bothWent():
                print("Waiting for the Player.......")
            else:
                os.system("clear")
                if 4 in game.sunk_ships:
                    print(f"Game Over! Player {game.sunk_ships.index(4)+1} Won")
                if game.turn == player:
                    os.system("clear")
                    print(f"It's your turn! You are player {player}")
                    time.sleep(2)
                    os.system("clear")
                    ui = ask_user_input(game.board_len,"Please type in your coordinate like H7: ",game.moves[player],[["" if type(game.moves[(player+1)%2][x][value]) == int else game.moves[(player+1)%2][x][value] for value in range(game.board_len)] for x in range(game.board_len)])
                    while game.moves[(player+1)%2][ui[0]][ui[1]] == "-" or game.moves[(player+1)%2][ui[0]][ui[1]] == "X":
                        os.system("clear")
                        print("You already guessed this coordinate")
                        ui = ask_user_input(game.board_len,"Please type in your coordinate like H7: ",game.moves[player],[["" if type(game.moves[(player+1)%2][x][value]) == int else game.moves[(player+1)%2][x][value] for value in range(game.board_len)] for x in range(game.board_len)])
                    if game.moves[(player+1)%2][ui[0]][ui[1]].isdigit():
                        os.system("clear")
                        print(f"{chr(65+ui[1])}{ui[0]+1} is a Hit\n")
                        temp_num = game.moves[(player+1)%2][ui[0]][ui[1]]
                        game.moves[(player+1)%2][ui[0]][ui[1]] = "X"
                        if not game.if_sunk_or_not(game.moves[(player+1)%2],temp_num):
                            print("Sunk")
                            game.sunk_ships[(player+1)%2] += 1
                    else:
                        os.system("clear")
                        print(f"{chr(65+ui[1])}{ui[0]+1} is a Miss\n")
                        game.moves[(player+1)%2][ui[0]][ui[1]] = "-"
                    game.turn = (player+1)%2
                else:
                    os.system("clear")
                    print(f"\n\n\n\nPlayer {(player+1)%2} is playing!\n\n\n\n")
                if not game.connected():
                    run = False
                

        except:
            run = False
            print("Couldn't get game")
            break

while True:
    main()