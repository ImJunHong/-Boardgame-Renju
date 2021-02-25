empty = 0
black = 1
white = 2
cell_amount = 19

class Rule(object):
    @staticmethod
    def is_valid(x, y):
        if 0 <= x < cell_amount and 0 <= y < cell_amount:
            return True
        return False

    def __init__(self, stones, log):
        self.stones = stones
        self.log = log
