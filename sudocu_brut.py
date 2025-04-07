s_map = [
[8,  7,  0,     0,  5,  9,      0,  0,  0],
[6,  5,  0,     0,  2,  8,      0,  0,  1],
[2,  1,  9,     4,  7,  6,      3,  5,  8],

[4,  9,  8,     7,  6,  3,      0,  0,  0],
[5,  6,  2,     9,  4,  1,      0,  0,  0],
[1,  3,  7,     5,  8,  2,      9,  4,  6],

[7,  8,  1,     2,  9,  4,      0,  0,  0],
[9,  2,  6,     8,  3,  5,      1,  7,  4],
[3,  4,  5,     6,  1,  7,      1,  0,  0]]


class Sudoku:
    solved = False

    def __init__(self, mapa):
        self.mapa = mapa

    def check_horisontal(self, row_i, num):
        row = self.mapa[row_i]
        if num in row:
            return False
        return True

    def check_vertikal(self, index, num):
        line = [self.mapa[i][index] for i in range(9)]
        if num in line:
            return False
        return True
        
    def do_const(self):
        self.const = []
        for i in range(9):
            self.const.append([i if i else continue for i in self.mapa])
My = Sudoku(s_map)

row_i = 0
for row in range(row_i,11):
    index = 0
    for index in range(index, 11):
        if My.mapa[row][index] != 0:
            continue
        else:
            for i in range(1,11):
                if i != 10:
                    if My.check_horisontal(row, i):
                        if My.check_vertikal(index, i):
                            My.mapa[row][index] = i
                            index+=1
                            break
                else : 
                    index-=1
                    if index > 0 :
                        index = 0
                        row_i -= 1



print(*My.mapa, sep="\n")