from tabulate import tabulate
import random
import os
from network import Network
import pickle
import time

board_len = 10
player_board = [["" for i in range(board_len)] for x in range(board_len)]
opponent_board = [["" for i in range(board_len)] for x in range(board_len)]
sunk_ships = 0

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



def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

def main():
    n = Network()
    player = int(n.getP())

    os.system("clear")
    print(f"=============================Welcome to the Python Battleship Game=============================\n\nYou are player {player}.\n\n")
    print("Please choose your ships for the board:")
    time.sleep(2)

    player_board = place_ships(opponent_board,board_len,player_board)
    
    run = True

    while run:
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

def main2():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

while True:
    main()