class Piece(object):
    def __init__(self, board, x, y, img):
        self.board = board
        self.x = x
        self.y = y
        self.img = img
        self.board[y][x] = self

class Pawn(Piece):
    def __init__(self, board, x, y, img):
        super().__init__(board, x, y, img)
        self.is_first_move = True

    def move(self, x, y):
        pass

class Knight(Piece):
    pass

class Rook(Piece):
    pass

class Bishop(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass