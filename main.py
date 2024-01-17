# Import and initialize the pg library
import pygame as pg
import random

def place_ships(com_board,board_len):
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
    return com_board

def if_sunk_or_not(com_board,num):
    return any(num in x for x in com_board)

def inititialize():

    pg.init()
    pg.font.init()



    global width , height
    width , height = 500,500

    global board_len
    board_len = 10

    global board, com_board
    board = [["" for i in range(board_len)] for x in range(board_len)]
    com_board = [["" for i in range(board_len)] for x in range(board_len)]
    com_board = place_ships(com_board,board_len)

    global basefont
    basefont = pg.font.Font(None,80)

    global last_turn, turns
    last_turn, turns = 30 , 0

    global sunk_ships
    sunk_ships = 0

    global screen
    screen = pg.display.set_mode((width, height))

    global temp_screen_dedicated
    temp_screen_dedicated = 435 // 10

    # pg.display.set_icon(pg.image.load('images/logo.ico'))
    pg.display.set_caption("Battleship")


    global fps
    fps = 30

    global clock
    clock = pg.time.Clock()
inititialize()
# Run until the user asks to quit
def placing_the_figure():
    for row in range(board_len):
        for col in range(board_len):
            if board[row][col] == "X":
                screen.blit(pg.transform.smoothscale(pg.image.load('images/hit.png'),(35,35)),(col*temp_screen_dedicated+40+col*2,row*temp_screen_dedicated+40+row*2))
            if board[row][col] == "-":
                screen.blit(pg.transform.smoothscale(pg.image.load('images/miss.png'),(35,35)),(col*temp_screen_dedicated+40+col*2,row*temp_screen_dedicated+40+row*2))

running = True
while running:
    # Did the user click the window close button?
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            Xpos,Ypos = pg.mouse.get_pos()
            print(Xpos,Ypos)
            if (Ypos >= 45 and Ypos <= 480) and (Xpos >= 45 and Xpos <= 480):
                ui = [int(Ypos//temp_screen_dedicated)-1,int(Xpos//temp_screen_dedicated)-1]
                print(ui)
                if not (com_board[min(board_len-1,ui[0])][min(board_len-1,ui[1])] == "-" or com_board[min(board_len-1,ui[0])][min(board_len-1,ui[1])] == "X"):
                    if com_board[min(board_len-1,ui[0])][min(board_len-1,ui[1])].isdigit():
                        temp_num = com_board[min(board_len-1,ui[0])][min(board_len-1,ui[1])]
                        board[min(board_len-1,ui[0])][min(board_len-1,ui[1])] = "X"
                        com_board[min(board_len-1,ui[0])][min(board_len-1,ui[1])] = "X"
                        if not if_sunk_or_not(com_board,temp_num):
                            sunk_ships += 1
                    else:
                        board[min(board_len-1,ui[0])][min(board_len-1,ui[1])] = "-"
                        com_board[min(board_len-1,ui[0])][min(board_len-1,ui[1])] = "-"

    background_image = pg.image.load("images/board.jpg")
    screen.blit(background_image,(0,0))
    placing_the_figure()
    # Flip the display
    pg.display.flip()

# Done! Time to quit.
pg.quit()