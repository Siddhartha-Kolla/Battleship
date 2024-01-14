class Game:
    def if_sunk_or_not(com_board,num):
        return any(num in x for x in com_board)