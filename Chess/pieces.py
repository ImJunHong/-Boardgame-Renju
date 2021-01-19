class Piece(object):
    def __init__(self, board, x, y, player, img):
        self.board = board
        self.x = x
        self.y = y
        self.player = player
        self.color = self.player.color
        self.img = img
        self.board[y][x] = self

    def move(self, x, y):
        if self.board[y][x]:
            self.board[y][x].player.piece_dict[self.board[y][x].__class__.__name__.lower()+"s"].remove(self.board[y][x])
        self.board[y][x] = self
        self.board[self.y][self.x] = None
        self.x = x
        self.y = y

    def is_movable(self, x, y, catchable=True, regardless_of_color=False):
        if x > 0:
            if self.x >= 8-x:
                return False
        else:
            if self.x <= -x-1:
                return False
        if self.color or regardless_of_color:
            if y > 0:
                if self.y >= 8-y:
                    return False
            else:
                if self.y <= -y-1:
                    return False
            if not catchable and self.board[self.y+y][self.x+x]:
                return False
            if self.board[self.y+y][self.x+x] and self.board[self.y+y][self.x+x].color == self.color:
                return False
            return self.x+x, self.y+y
        else:
            if y > 0:
                if self.y <= y-1:
                    return False
            else:
                if self.y >= 8+y:
                    return False
            if not catchable and self.board[self.y-y][self.x+x]:
                return False
            if self.board[self.y-y][self.x+x] and self.board[self.y-y][self.x+x].color == self.color:
                return False
            return self.x+x, self.y-y

    def get_loc(self, value):
        if self.color:
            return value
        else:
            return 7-value

    def get_dis(self, value):
        if self.color:
            return value
        else:
            return -value

    def is_valid(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        return False

class Pawn(Piece):
    def __init__(self, board, x, y, player, img):
        super().__init__(board, x, y, player, img)
        self.is_first_move = True

    def get_movables(self):
        movables = []
        # 앞으로 한 칸 이동
        coord = self.is_movable(0, -1, catchable=False)
        if coord: movables.append(coord)
        # 첫 번째 행마일 경우 앞으로 두 칸 이동 가능
        if self.is_first_move:
            coord = self.is_movable(0, -2, catchable=False)
            if coord:
                cx, cy = coord
                if not self.board[cy+self.get_dis(1)][cx]:
                    movables.append(coord)
        # 대각선 한 칸 이동
        coord = self.is_movable(-1, -1)
        if coord:
            cx, cy = coord
            if self.board[cy][cx] and self.board[cy][cx].color != self.color:
                movables.append(coord)
        coord = self.is_movable(1, -1)
        if coord:
            cx, cy = coord
            if self.board[cy][cx] and self.board[cy][cx].color != self.color:
                movables.append(coord)

        return movables

    def move(self, x, y):
        super().move(x, y)
        if self.is_first_move:
            self.is_first_move = False

class Knight(Piece):
    def get_movables(self):
        movables = []
        coords = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]
        for cx, cy in coords:
            coord = self.is_movable(cx, cy)
            if coord: movables.append(coord)
        return movables

class Rook(Piece):
    def get_movables(self):
        movables = []
        coords = []

        x, y = self.x, self.y
        xx, yy = 0, 0
        while x > 0:
            xx -= 1
            x -= 1
            coords.append((xx, yy))
            if self.board[y][x]: break

        x, y = self.x, self.y
        xx, yy = 0, 0
        while x < 7:
            xx += 1
            x += 1
            coords.append((xx, yy))
            if self.board[y][x]: break

        x, y = self.x, self.y
        xx, yy = 0, 0
        while y > 0:
            yy -= 1
            y -= 1
            coords.append((xx, yy))
            if self.board[y][x]: break

        x, y = self.x, self.y
        xx, yy = 0, 0
        while y < 7:
            yy += 1
            y += 1
            coords.append((xx, yy))
            if self.board[y][x]: break

        for cx, cy in coords:
            coord = self.is_movable(cx, cy, regardless_of_color=True)
            if coord: movables.append(coord)
        return movables

class Bishop(Piece):
    def get_movables(self):
        movables = []
        coords = []

        x, y = self.x, self.y
        xx, yy = 0, 0
        while x > 0 and y > 0:
            xx -= 1
            x -= 1
            yy -= 1
            y -= 1
            coords.append((xx, yy))
            if self.board[y][x]: break
        
        x, y = self.x, self.y
        xx, yy = 0, 0
        while x < 7 and y > 0:
            xx += 1
            x += 1
            yy -= 1
            y -= 1
            coords.append((xx, yy))
            if self.board[y][x]: break

        x, y = self.x, self.y
        xx, yy = 0, 0
        while x > 0 and y < 7:
            xx -= 1
            x -= 1
            yy += 1
            y += 1
            coords.append((xx, yy))
            if self.board[y][x]: break

        x, y = self.x, self.y
        xx, yy = 0, 0
        while x < 7 and y < 7:
            xx += 1
            x += 1
            yy += 1
            y += 1
            coords.append((xx, yy))
            if self.board[y][x]: break

        for cx, cy in coords:
                coord = self.is_movable(cx, cy, regardless_of_color=True)
                if coord: movables.append(coord)
        return movables

class Queen(Piece):
    def get_movables(self):
        movables = []
        movables += Rook(self.board, self.x, self.y, self.player, self.img).get_movables()
        movables += Bishop(self.board, self.x, self.y, self.player, self.img).get_movables()
        self.board[self.y][self.x] = self
        return movables

class King(Piece):
    def get_movables(self):
        movables = []
        coords = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for cx, cy in coords:
            coord = self.is_movable(cx, cy)
            if coord: movables.append(coord)
        return movables