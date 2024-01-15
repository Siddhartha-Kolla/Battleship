from tabulate import tabulate
import random
import os

"""My category"""
def create_table(board_len,data):
    
    # Table to print the players board
    header = [chr(65+i) for i in range(board_len)]
    board_index = range(1,board_len+1)
    table = tabulate(data,tablefmt="rounded_grid",showindex=board_index,headers=header)
    return table

def ask_user_input(board_len, message,board,com_board):
    print(tabulate([[create_table(board_len,board), create_table(board_len,com_board)]], rowalign="center", tablefmt="grid"))
    user_input = input(message).strip()
    while not(int(user_input[1:])-1 < board_len and ord(user_input[0].upper())-65 < board_len):
        user_input = input("Incorrect Coordinate!! Please type in your coordinate like H7: ").strip()
    return [int(user_input[1:])-1,ord(user_input[0].upper())-65]

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

def if_sunk_or_not(com_board,num):
    return any(num in x for x in com_board)

os.system("clear")
print("=============================Welcome to the Python Battleship Game=============================\n\n")




def game_loop(board_len):
    sunk_ships = 0
    last_turn = 30
    turns = 0
    # Player board
    board_len = 10
    board = [["" for i in range(board_len)] for x in range(board_len)]
    com_board = [["" for i in range(board_len)] for x in range(board_len)]
    com_board = place_ships(com_board,board_len,board)
    while sunk_ships != 4 and turns <= last_turn:
        turns += 1
        ui = ask_user_input(board_len,"Please type in your coordinate like H7: ",board,com_board)
        while board[ui[0]][ui[1]] == "-" or board[ui[0]][ui[1]] == "X":
            os.system("clear")
            print("You already guessed this coordinate")
            ui = ask_user_input(board_len,"Please type in your coordinate like H7: ",board,com_board)
        if com_board[ui[0]][ui[1]].isdigit():
            os.system("clear")
            print(f"{chr(65+ui[1])}{ui[0]+1} is a Hit\n")
            temp_num = com_board[ui[0]][ui[1]]
            board[ui[0]][ui[1]] = "X"
            com_board[ui[0]][ui[1]] = "X"
            if not if_sunk_or_not(com_board,temp_num):
                print("Sunk")
                sunk_ships += 1
        else:
            os.system("clear")
            print(f"{chr(65+ui[1])}{ui[0]+1} is a Miss\n")
            board[ui[0]][ui[1]] = "-"
            com_board[ui[0]][ui[1]] = "-"
    if sunk_ships == 4:
        print(f"You have won the game with {turns} moves")
    else:
        print(f"Oh no!! You have lost the Battleship game with {sunk_ships} ships sunk and {turns} moves")

            


game_loop(10)