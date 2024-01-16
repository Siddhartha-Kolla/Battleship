from tabulate import tabulate
board_len = 10
board = [["" for i in range(board_len)] for x in range(board_len)]
def create_table(board_len,data):
    
    # Table to print the players board
    header = [chr(65+i) for i in range(board_len)]
    board_index = range(1,board_len+1)
    table = tabulate(data,tablefmt="rounded_grid",showindex=board_index,headers=header)
    return table

table1 = create_table(board_len,board)
# print(f"{table1}   {table1}")
print(tabulate([[table1, table1]], rowalign="center", tablefmt="grid"))

print(-1%2)

lst = [["","","","","","","",""],["","","","","","","x",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]
print(lst)
lst = [[2 if lst[x][value] == "" else "None" for value in range(len(lst[0]))] for x in range(len(lst))]
print(lst,type(lst) == list())