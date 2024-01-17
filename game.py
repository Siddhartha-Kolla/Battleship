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
    def if_sunk_or_not(com_board,num,a):
        return any(num in x for x in com_board)
    def connected(self):
        return self.ready
    def bothWent(self):
        return self.Went[0] and self.Went[1]
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
    def play(self, player, player_board):
        self.Went[player] = True
        self.moves[player] = player_board
    def check(self,player,ui):
        if self.moves[(player+1)%2][ui[0]][ui[1]] == "-" or self.moves[(player+1)%2][ui[0]][ui[1]] == "X":
            return "-X"
    def hit_or_miss(self,player,ui):
        if self.moves[(player+1)%2][ui[0]][ui[1]] == "-" or self.moves[(player+1)%2][ui[0]][ui[1]] == "X":
            return "-X"
        if self.moves[(player+1)%2][ui[0]][ui[1]].isdigit():
            temp_num = self.moves[(player+1)%2][ui[0]][ui[1]]
            self.moves[(player+1)%2][ui[0]][ui[1]] = "X"
            temp_var = self.moves[(player+1)%2]
            if not any(temp_num in x for x in temp_var):
                self.sunk_ships[(player+1)%2] += 1
                return "S"
            return "H"
        else:
            self.moves[(player+1)%2][ui[0]][ui[1]] = "-"
            return "M"