from tabulate import tabulate
import random
import os
class Game:
    def __init__(self, id):
        self.Went = [False,False]
        self.board_len = 10
        self.ready = False
        self.id = id
        self.moves = [[["" for i in range(self.board_len)] for x in range(self.board_len)], [["" for i in range(self.board_len)] for x in range(self.board_len)]]
        self.sunk_ships = [0,0]
        self.turn = 0
    def if_sunk_or_not(com_board,num):
        return any(num in x for x in com_board)
    def connected(self):
        return self.ready
    def bothWent(self):
        return self.Went[0] and self.Went[1]
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
    def play(self, player):
        if player == 0:
            self.Went[0] = True
        else:
            self.Went[1] = True
    def hit_or_miss(self,player,ui):
        if self.moves[(player+1)%2][ui[0]][ui[1]].isdigit():
            temp_num = self.moves[(player+1)%2][ui[0]][ui[1]]
            self.moves[(player+1)%2][ui[0]][ui[1]] = "X"
            if not self.if_sunk_or_not(self.moves[(player+1)%2],temp_num):
                print("Sunk")
                self.sunk_ships[(player+1)%2] += 1
        else:
            self.moves[(player+1)%2][ui[0]][ui[1]] = "-"
        self.turn = (player+1)%2