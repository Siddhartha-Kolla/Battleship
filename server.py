import socket
from _thread import *
import pickle
from game import Game

print("Hello")
server = "192.168.137.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048*6))

            if gameId in games:

                if not data:
                    break
                elif data == "get":
                    print("Yes")
                    game = games[gameId]
                    conn.sendall(pickle.dumps(game))
                elif "play" in data and type(data) == tuple:
                    game = games[gameId]
                    game.play(p,data[1])
                    conn.sendall(pickle.dumps(game))
                elif "check" in data and type(data) == tuple:
                    game = games[gameId]
                    c = game.check(p,data[1])
                    conn.sendall(pickle.dumps(c))
                elif data == "bothwent":
                    game = games[gameId]
                    conn.sendall(pickle.dumps(game.bothWent()))
                elif data == "sunkships":
                    game = games[gameId]
                    conn.sendall(pickle.dumps(game.sunk_ships))
                elif data == "turn":
                    game = games[gameId]
                    conn.sendall(pickle.dumps(game.turn))
                elif data == "getplayerboards":
                    game = games[gameId]
                    conn.sendall(pickle.dumps(game.moves))
                elif type(data) == list:
                    print("Yes")
                    game = games[gameId]
                    print(p,data,game.hit_or_miss(p,data))
                    conn.sendall(pickle.dumps(game.hit_or_miss(p,data)))
                elif data == "changeturn":
                    game = games[gameId]
                    print(f"Changing turn {game.turn}")
                    game.turn = (p+1)%2
                    print(f"Now turn {game.turn}")
                elif data == "connected":
                    conn.sendall(pickle.dumps(game.connected()))
                else:

                    conn.sendall(None)
            else:
                break
        except Exception as e:
            print("Error catched", e)
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))