from tabulate import tabulate
import random

# Player board
board_len = 10

board = [["" for i in range(board_len)] for x in range(board_len)]
com_board = [["" for i in range(board_len)] for x in range(board_len)]

def create_table(board_len,data):
    
    # Table to print the players board
    header = [chr(65+i) for i in range(board_len)]
    board_index = range(1,board_len+1)
    table = tabulate(data,tablefmt="rounded_grid",showindex=board_index,headers=header)
    return table

# def place_ships(com_board):
    
for i in range(2,6):

    pos_ok = False
    while not pos_ok:
        
        pos = (random.randrange(board_len),random.randrange(board_len))
        orientation = random.choice(["vertical","horizontal"])
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


# com_board = place_ships(com_board)
print(create_table(board_len,board))
print(create_table(board_len,com_board))


print("Welcome to the Python Battleship Game\n\n")

def if_sunk_or_not(com_board,num):
    return any(num in x for x in com_board)

def ask_user_input(board_len):
    user_input = input("Please type in your coordinate like H7: ").strip()
    while not(int(user_input[1]) < board_len and ord(user_input[0])-65 < board_len):
        user_input = input("Incorrect Coordinate!! Please type in your coordinate like H7: ").strip()
    return [int(user_input[1]),ord(user_input[0])-65]


def game_loop(board_len):
    sunk_ships = 0
    while sunk_ships != 4:
        ui = ask_user_input(board_len)
        if com_board[ui[0]][ui[1]].isdigit():
            print("Hit")
            


game_loop(board_len)