EMPTY = 0
BLACK = 1
WHITE = 2
MAX = 19

class Block(object):
    def __init__(self, x, y):
        self.coords = [(x, y)]
        self.borders = []

def is_valid(stones, x, y, color, board_log):
    if not (0 <= x < MAX and 0 <= y < MAX):
        return False
    elif is_forbidden(stones, x, y, color, board_log):
        return False
    return True

def is_forbidden(stones, x, y, color, board_log):
    # 패(覇)
    if len(board_log) >= 2:
        prev_board = board_log[-1]
        ENEMY = get_enemy(color)
        stones[y][x] = color
        capture(stones, color)
        curr_board = to_string(stones)
        restore_board(stones, prev_board)
        if curr_board == board_log[-2]:
            return True

    # suicide 금지
    ENEMY = get_enemy(color)
    stones[y][x] = color
    captured = capture(stones, ENEMY, change_board=False)
    captured_enemy = capture(stones, color, change_board=False)
    stones[y][x] = EMPTY
    if (x, y) in captured:
        if captured_enemy:
            return False
        return True
    return False

def is_countable(stones):
    empty_blocks = search_blocks(stones, EMPTY)
    if len(empty_blocks) <= 1:
        return False
    for block in empty_blocks:
        first_color = 0
        for x, y in block.borders:
            if x != 0 and stones[y][x-1] > EMPTY:
                if first_color == 0:
                    first_color = stones[y][x-1]
                elif first_color != stones[y][x-1]:
                    return False
            if x != MAX-1 and stones[y][x+1] > EMPTY:
                if first_color == 0:
                    first_color = stones[y][x+1]
                elif first_color != stones[y][x+1]:
                    return False
            if y != 0 and stones[y-1][x] > EMPTY:
                if first_color == 0:
                    first_color = stones[y-1][x]
                elif first_color != stones[y-1][x]:
                    return False
            if y != MAX-1 and stones[y+1][x] > EMPTY:
                if first_color == 0:
                    first_color = stones[y+1][x]
                elif first_color != stones[y+1][x]:
                    return False
    return count_territory(stones, empty_blocks)

def count_territory(stones, blocks):
    scores = [None, 0, 0]
    for block in blocks:
        first_color = 0
        for x, y in block.borders:
            if x != 0 and stones[y][x-1] > EMPTY:
                if first_color == 0:
                    first_color = stones[y][x-1]
                    break
            if x != MAX-1 and stones[y][x+1] > EMPTY:
                if first_color == 0:
                    first_color = stones[y][x+1]
                    break
            if y != 0 and stones[y-1][x] > EMPTY:
                if first_color == 0:
                    first_color = stones[y-1][x]
                    break
            if y != MAX-1 and stones[y+1][x] > EMPTY:
                if first_color == 0:
                    first_color = stones[y+1][x]
                    break
        scores[first_color] += len(block.coords)
    return scores

def get_enemy(color):
    if color == BLACK:
        return WHITE
    elif color == WHITE:
        return BLACK
    else:
        return EMPTY

def to_string(stones):
    string = ""
    for x in range(MAX):
        for y in range(MAX):
            string += str(stones[y][x])
    return string

def restore_board(stones, string):
    for x in range(MAX):
        for y in range(MAX):
            stones[y][x] = int(string[x*MAX+y])

def capture(stones, color, change_board=True):
    blocks = search_blocks(stones, color)
    captured = []
    for block in blocks:
        is_captured = True
        for x, y in block.borders:
            if x != 0 and stones[y][x-1] == EMPTY:
                is_captured = False
                break
            if x != MAX-1 and stones[y][x+1] == EMPTY:
                is_captured = False
                break
            if y != 0 and stones[y-1][x] == EMPTY:
                is_captured = False
                break
            if y != MAX-1 and stones[y+1][x] == EMPTY:
                is_captured = False
                break
        if is_captured:
            for x, y in block.coords:
                if change_board:
                    stones[y][x] = 0
                captured.append((x, y))
    return captured

def search_blocks(stones, color):
    ENEMY = get_enemy(color)
    coords = [(x, y) for x in range(MAX) for y in range(MAX) if stones[y][x] == ENEMY]
    blocks = []
    while coords:
        for x, y in coords:
            if stones[y][x] == ENEMY:
                block = Block(x, y)
                coords.remove((x, y))
                search_stones(stones, coords, block, x, y)
                blocks.append(block)
                break
    search_borders(stones, blocks)
    return blocks

def search_stones(stones, coords, block, x, y):
    if x < MAX-1 and stones[y][x+1] == stones[y][x] and (x+1, y) in coords and (x+1, y) not in block.coords:
        coords.remove((x+1, y))
        block.coords.append((x+1, y))
        search_stones(stones, coords, block, x+1, y)

    if y < MAX-1 and stones[y+1][x] == stones[y][x] and (x, y+1) in coords and (x, y+1) not in block.coords:
        coords.remove((x, y+1))
        block.coords.append((x, y+1))
        search_stones(stones, coords, block, x, y+1)

    if x > 0 and stones[y][x-1] == stones[y][x] and (x-1, y) in coords and (x-1, y) not in block.coords:
        coords.remove((x-1, y))
        block.coords.append((x-1, y))
        search_stones(stones, coords, block, x-1, y)

    if y > 0 and stones[y-1][x] == stones[y][x] and (x, y-1) in coords and (x, y-1) not in block.coords:
        coords.remove((x, y-1))
        block.coords.append((x, y-1))
        search_stones(stones, coords, block, x, y-1)

def search_borders(stones, blocks):
    for block in blocks:
        for x, y in block.coords:
            if not (0 < x < MAX-1 and 0 < y < MAX-1) or\
                    not (stones[y][x+1] == stones[y][x] and stones[y][x-1] == stones[y][x] and stones[y+1][x] == stones[y][x] and stones[y-1][x] == stones[y][x]):
                block.borders.append((x, y))