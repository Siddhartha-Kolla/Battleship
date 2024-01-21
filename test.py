    # Simple pygame program

    # Import and initialize the pygame library
import pygame as pg
import multiprocessing

def window_draw():
    pg.init()

    # Set up the drawing window
    screen = pg.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pg.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Flip the display
        pg.display.flip()

    # Done! Time to quit.
    pg.quit()

if __name__ == '__main__':
    p1 = multiprocessing.Process(name='p1', target=window_draw)
    p = multiprocessing.Process(name='p', target=window_draw)
    p1.start()
    p.start()


import socket
import keyboard


host = "192.168.137.1"
port = 5555
server = socket.socket()
server.bind((host,port))
server.listen()
conn, addr = server.accept()
print(conn)
print ("Connection from: " + str(addr))

while True:
    data = conn.recv(2048).decode()
    if keyboard.read_key() == "i":
        user_input = input("Enter your input: ")
        conn.sendall(user_input)
    else:
        user_input = ""
    if not data:
        continue
    else:
        print(f"Message from the other user: {data}")