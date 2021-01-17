empty = 0
black = 1
white = 2
directions = [(0, -1), (1, -1), (1, 0), (1, 1)]

class Rule(object):
    def __init__(self, stones, log):
        self.stones = stones
        self.log = log

    def is_valid(self, x, y):
        if 0 <= x < 15 and 0 <= y < 15:
            return True
        return False
    
    def check_forbiddens(self):
        forbiddens = []
        for x in range(15):
            for y in range(15):
                if self.stones[y][x] == empty and self.is_forbidden(x, y):
                    forbiddens.append((x, y))
        return forbiddens

    def is_forbidden(self, x, y):
        if self.is_five(x, y):
            return False
        elif self.is_jangmok(x, y) or self.is_fours(x, y) or self.is_threes(x, y):
            return True
        return False

    def count_stones(self, x, y, direction, color=black):
        dx, dy = directions[direction]
        xx, yy = x, y
        count = 1
        for i in range(2):
            x, y = xx, yy
            x += dx*(-1)**i
            y += dy*(-1)**i
            while self.is_valid(x, y) and self.stones[y][x] == color:
                x += dx*(-1)**i
                y += dy*(-1)**i
                count += 1
        return count

    def find_empty(self, x, y, direction, i):
        dx, dy = directions[direction]
        dx *= (-1)**i
        dy *= (-1)**i
        while self.is_valid(x, y) and self.stones[y][x] == black:
            x += dx
            y += dy
        if self.is_valid(x, y) and self.stones[y][x] == empty:
            return x, y
        return None

    def is_jangmok(self, x, y):
        for direction in range(4):
            count = self.count_stones(x, y, direction)
            if count > 5:
                return True
        return False

    def is_five(self, x, y, direction=None, color=black):
        if direction:
            if self.count_stones(x, y, direction) == 5:
                return True
        else:
            for direction in range(4):
                count = self.count_stones(x, y, direction, color)
                if count == 5:
                    return True
        return False

    def is_four(self, x, y, direction):
        for i in range(2):
            coord = self.find_empty(x, y, direction, i)
            if coord:
                if self.is_five(coord[0], coord[1], direction):
                    return True

    def check_open_four(self, x, y, direction):
        if self.is_five(x, y):
            return False
        count = 0
        for i in range(2):
            coord = self.find_empty(x, y, direction, i)
            if coord:
                if self.is_five(coord[0], coord[1], direction):
                    count += 1
        if count == 2: # ●○●○●○● → ●○●●●○● 이런 경우처럼 한 번의 착수로 같은 direction에서 2개의 4가 생기는 경우에만 해당됨
            if self.count_stones(x, y, direction) == 4: # 일반적인 open four
                count = 1
        else:
            count = 0
        return count

    def check_open_three(self, x, y, direction):
        xx, yy = x, y
        for i in range(2):
            x, y = xx, yy
            coord = self.find_empty(x, y, direction, i)
            if coord:
                x, y = coord
                self.stones[y][x] = black
                # 돌을 추가하였을 때 open four가 되는가?
                if self.check_open_four(x, y, direction) == 1:
                    # 돌을 추가한 자리가 다른 이유에 의해 금수가 되어 돌을 추가할 수 없는 자리가 되는가?
                    if not self.is_forbidden(x, y):
                        self.stones[y][x] = empty
                        return True
                self.stones[y][x] = empty
        return False

    def is_fours(self, x, y):
        count = 0
        self.stones[y][x] = black
        for direction in range(4):
            # 같은 direction에서 두 개의 4가 생길 때
            if self.check_open_four(x, y, direction) == 2:
                count += 2
            # 해당 direction에서 한 개의 4가 생길 때
            elif self.is_four(x, y, direction):
                count += 1
        self.stones[y][x] = empty
        if count >= 2:
            return True
        return False

    def is_threes(self, x, y):
        count = 0
        self.stones[y][x] = black
        for direction in range(4):
            if self.check_open_three(x, y, direction):
                count += 1
        self.stones[y][x] = empty
        if count >= 2:
            return True
        return False