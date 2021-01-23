class Piece(object):
    def __init__(self, board, x, y, player, img):
        self.board = board
        self.x = x
        self.y = y
        self.player = player
        self.color = self.player.color
        self.img = img
        self.is_moved = False
        self.board[y][x] = self

    def move(self, x, y):
        if self.board[y][x]:
            self.board[y][x].player.piece_dict[self.board[y][x].kind+"s"].remove(self.board[y][x])
        self.board[y][x] = self
        self.board[self.y][self.x] = None
        self.x = x
        self.y = y
        if not self.is_moved:
            self.is_moved = True

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
        self.kind = "pawn"

    def get_movables(self):
        movables = []
        # 앞으로 한 칸 이동
        coord = self.is_movable(0, -1, catchable=False)
        if coord: movables.append(coord)
        # 첫 번째 행마일 경우 앞으로 두 칸 이동 가능
        if not self.is_moved:
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

    def is_promotionable(self, movables):
        promotionables = []
        for x, y in movables:
            if y == self.get_loc(0):
                promotionables.append((x, y))
        return promotionables

    def is_en_passantable(self, log):
        if log[-1] == "normal":
            py = log[0][1]
            cx, cy = log[1]
            if abs(py-cy) == 2 and ((self.x, self.y) == (cx-1, cy) or (self.x, self.y) == (cx+1, cy)):
                return cx, (py+cy)//2
        return None

class Knight(Piece):
    def __init__(self, board, x, y, player, img):
        super().__init__(board, x, y, player, img)
        self.kind = "knight"

    def get_movables(self):
        movables = []
        coords = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]
        for cx, cy in coords:
            coord = self.is_movable(cx, cy)
            if coord: movables.append(coord)
        return movables

class Rook(Piece):
    def __init__(self, board, x, y, player, img):
        super().__init__(board, x, y, player, img)
        self.kind = "rook"

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
    def __init__(self, board, x, y, player, img):
        super().__init__(board, x, y, player, img)
        self.kind = "bishop"
        
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
    def __init__(self, board, x, y, player, img):
        super().__init__(board, x, y, player, img)
        self.kind = "queen"
        
    def get_movables(self):
        movables = []
        movables += Rook(self.board, self.x, self.y, self.player, self.img).get_movables()
        movables += Bishop(self.board, self.x, self.y, self.player, self.img).get_movables()
        self.board[self.y][self.x] = self
        return movables

class King(Piece):
    def __init__(self, board, x, y, player, img):
        super().__init__(board, x, y, player, img)
        self.kind = "king"
        
    def get_movables(self):
        movables = []
        coords = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for cx, cy in coords:
            coord = self.is_movable(cx, cy)
            if coord: movables.append(coord)
        return movables

    def is_castleable(self):
        # 킹이 한 번도 움직이지 않았을 때
        if not self.is_moved:
            # 킹의 체크 여부 확인
            if self.is_attacked(4, self.get_loc(7)):
                return False
            rooks = self.player.piece_dict["rooks"]
            castleable_rooks = []
            for rook in rooks:
                # 룩이 한 번도 움직이지 않았을 때
                if not rook.is_moved:
                    castleable_rooks.append(rook)
            coords = []
            for rook in castleable_rooks:
                y = self.get_loc(7)
                # 퀸 사이드 캐슬링
                if rook.x == 0:
                    count = 0
                    for x in range(1, 4):
                        if self.board[y][x] == None:
                            count += 1
                    # 킹이 이동하는 경로가 공격당하는지 여부 확인
                    if count == 3 and not self.is_attacked(2, y) and not self.is_attacked(3, y):
                        coords.append((2, y))
                # 킹 사이드 캐슬링
                else:
                    count = 0
                    for x in range(5, 7):
                        if self.board[y][x] == None:
                            count += 1
                    # 킹이 이동하는 경로가 공격당하는지 여부 확인
                    if count == 2 and not self.is_attacked(5, y) and not self.is_attacked(6, y):
                        coords.append((6, y))
        else:
            return False
        return coords

    def is_attacked(self, x, y):
        for pieces in self.player.opponent.piece_dict.values():
            for piece in pieces:
                if (x, y) in piece.get_movables():
                    return True
        return False