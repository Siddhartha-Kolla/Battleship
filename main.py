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