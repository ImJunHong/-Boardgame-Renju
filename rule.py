empty = 0
black = 1
directions = [(0, -1), (1, -1), (1, 0), (1, 1)]
forbiddens = []

class Rule(object):
    def __init__(self, stones, log):
        self.stones = stones
        self.log = log

    def check_validality(self, x, y):
        if 0 <= x < 15 and 0 <= y < 15:
            return True
        return False

    def check_forbiddens(self):
        for x in range(15):
            for y in range(15):
                if self.stones[y][x] == empty:
                    pass
                    
    def count_stones(self, x, y, direction, color=black, need_shape=False):
        count = 0
        shape = ""
        xx, yy = directions[direction]
        for i in range(-2, 3):
            if self.check_validality(x + xx*i, y + yy*i):
                if self.stones[y + yy*i][x + xx*i] == color:
                    count += 1
                    shape += "O"
                elif self.stones[y + yy*i][x + xx*i] == empty:
                    shape += "X"
                else:
                    shape += "Z"
            else:
                return 0, ""
        if need_shape:
            return count, shape
        return count

    def is_five(self, x, y, direction, color):
        count = self.count_stones(x, y, direction, color=color)
        if count == 5:
            return True
        return False

    def is_open_four(self, x, y, direction):
        count, shape = self.count_stones(x, y, direction, need_shape=True)
        xx, yy = directions[direction]
        if count == 4:
            if shape == "XOOOO":
                if self.check_validality(x + 3*xx, y + 3*yy) and self.stones[y + 3*yy][x + 3*xx] == empty:
                    return True
            elif shape == "OOOOX":
                if self.check_validality(x - 3*xx, y - 3*yy) and self.stones[y - 3*yy][x - 3*xx] == empty:
                    return True
        return False

    def is_open_three(self, x, y, direction):
        count, shape = self.count_stones(x, y, direction, need_shape=True)
        xx, yy = directions[direction]
        if count == 3:
            result = False
            if shape in ["XXOOO", "OXOOX"]:
                self.stones[y - yy][x - xx] = black
                if self.is_open_four(x, y, direction):
                    result = True
                self.stones[y - yy][x - xx] = empty
            elif shape in ["XOXOO", "OOXOX"]:
                self.stones[y][x] = black
                if self.is_open_four(x, y, direction):
                    result = True
                self.stones[y][x] = empty
            elif shape in ["OOOXX", "XOOXO"]:
                self.stones[y + yy][x + xx] = black
                if self.is_open_four(x, y, direction):
                    result = True
                self.stones[y + yy][x + xx] = empty
            elif shape == "XOOOX":
                self.stones[y - 2*yy][x - 2*xx] = black
                if self.is_open_four(x, y, direction):
                    result = True
                    self.stones[y - 2*yy][x - 2*xx] = empty
                else:
                    self.stones[y - 2*yy][x - 2*xx] = empty
                    self.stones[y + 2*yy][x + 2*xx] = black
                    if self.is_open_four(x, y, direction):
                        result = True
                    self.stones[y + 2*yy][x + 2*xx] = empty
            if result:
                return True
        return False