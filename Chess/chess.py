import pygame as pg
import sys
from pieces import *

background_color = ( 60,  10,   0)
black            = (  0,   0,   0)
greyblue         = (140, 170, 200)
white            = (255, 255, 255)
red              = (255,   0,   0)
grey             = (255, 225, 225, 150)
pink             = (255, 200, 225)
lightgreen       = (155, 230, 205)
lime             = (191, 255,   0)
yellow           = (250, 225,  20)
purple           = (128,   0, 128)

scr_size = 900
sq_size = 100
mg = 50
color_list = ["black", "white"]
piece_list = ["pawn", "knight", "rook", "bishop", "queen", "king"]

fps = 60
clock = pg.time.Clock()

def main():
    pg.init()
    screen = pg.display.set_mode([scr_size, scr_size])
    pg.display.set_caption("Chess")
    game = Game(screen)

class Player(object):
    def __init__(self, board, color, imgs):
        self.board = board
        self.color = color # True 백, False 흑
        self.piece_dict = {"pawns":[], "knights":[], "rooks":[], "bishops":[], "queens":[], "kings":[]}
        self.set_pieces(imgs)

    def set_loc(self, value):
        if self.color:
            return value
        else:
            return 7-value

    def set_pieces(self, imgs):
        if self.color: idx = 6
        else: idx = 0
        for i in range(8):
            self.piece_dict["pawns"].append(Pawn(self.board, i, self.set_loc(6), self, imgs[idx]))
        for i in range(2):
            self.piece_dict["knights"].append(Knight(self.board, 5*i+1, self.set_loc(7), self, imgs[idx+1]))
            self.piece_dict["rooks"].append(Rook(self.board, 7*i, self.set_loc(7), self, imgs[idx+2]))
            self.piece_dict["bishops"].append(Bishop(self.board, 3*i+2, self.set_loc(7), self, imgs[idx+3]))
        self.piece_dict["queens"].append(Queen(self.board, 3, self.set_loc(7), self, imgs[idx+4]))
        self.piece_dict["kings"].append(King(self.board, 4, self.set_loc(7), self, imgs[idx+5]))

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.temp_screen = screen.convert_alpha()
        self.is_gameover = False
        self.winner = 0
        self.turn = True
        self.initialize_variables()
        self.board = [[None for y in range(8)] for x in range(8)]
        self.log = []
        self.board_log = []
        self.fifty_move_log = [0]
        self.font = pg.font.SysFont("새굴림", 14)
        self.imgs = self.load_images()
        self.set_players()
        self.play_game(screen)
    
    def load_images(self):
        imgs = []
        for color in color_list:
            for piece in piece_list:
                imgs.append(pg.transform.scale(pg.image.load("Chess/images/"+color+"_"+piece+".png"), (sq_size, sq_size)))
        return imgs

    def set_players(self):
        self.white_player = Player(self.board, True, self.imgs)
        self.black_player = Player(self.board, False, self.imgs)
        self.white_player.opponent = self.black_player
        self.black_player.opponent = self.white_player

    def print_text(self, msg, color, pos):
        textSurface = self.font.render(msg, True, color, None)
        textRect = textSurface.get_rect()
        textRect.center = pos
        self.screen.blit(textSurface, textRect)

    def initialize_variables(self):
        self.selected = None
        self.selected_movables = None
        self.castleables = None
        self.promotionables = None
        self.en_passant = None

    def get_xy(self, pos):
        x, y = pos
        x = (x-mg)//sq_size
        y = (y-mg)//sq_size
        return x, y

    def set_xy(self, x, y):
        self.board[y][x].x = x
        self.board[y][x].y = y

    def real_xy(self, x):
        return mg + x*sq_size

    def add_to_dict(self, piece):
        piece.player.piece_dict[piece.kind+"s"].append(piece)

    def remove_from_dict(self, piece):
        piece.player.piece_dict[piece.kind+"s"].remove(piece)

    def is_valid(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        return False
    
    def draw_board(self, screen):
        pg.draw.rect(screen, white, [mg, mg, 8*sq_size, 8*sq_size])
        for i in range(8):
            for j in range(4):
                pg.draw.rect(screen, greyblue, [self.real_xy((j*2+(i+1)%2)), self.real_xy(i), sq_size, sq_size])
        bdr = 4
        pg.draw.rect(screen, black, [mg-bdr, mg-bdr, 8*sq_size+bdr*2, 8*sq_size+bdr*2], bdr)

    def draw_selected(self, screen):
        if self.selected:
            x = self.selected.x
            y = self.selected.y
            pg.draw.rect(screen, pink, [self.real_xy(x), self.real_xy(y), sq_size, sq_size])

            self.selected_movables = self.selected.get_movables()
            for mx, my in self.selected_movables:
                if self.board[my][mx] and self.board[my][mx].kind == "king":
                    pg.draw.rect(screen, yellow, [self.real_xy(mx), self.real_xy(my), sq_size, sq_size])
                else:
                    pg.draw.rect(screen, lightgreen, [self.real_xy(mx), self.real_xy(my), sq_size, sq_size])

            if self.selected.kind == "king":
                self.castleables = self.selected.is_castleable()
                if self.castleables:
                    for x, y in self.castleables:
                        pg.draw.rect(screen, lime, [self.real_xy(x), self.real_xy(y), sq_size, sq_size])
                        self.print_text("Castling", black, [self.real_xy(x)+sq_size//2, self.real_xy(y)+sq_size//2])
            elif self.selected.kind == "pawn":
                self.promotionables = self.selected.is_promotionable(self.selected_movables)
                if self.log:
                    self.en_passant = self.selected.is_en_passantable(self.log[-1])
                    if self.en_passant:
                        x, y = self.en_passant
                        pg.draw.rect(screen, lime, [self.real_xy(x), self.real_xy(y), sq_size, sq_size])
                        self.print_text("En Passant", black, [self.real_xy(x)+sq_size//2, self.real_xy(y)+sq_size//2])

    def draw_pieces(self, screen):
        for x in range(8):
            for y in range(8):
                if self.board[y][x]:
                    self.screen.blit(self.board[y][x].img, (self.real_xy(x), self.real_xy(y)))

    def click(self, screen, pos):
        x, y = self.get_xy(pos)
        if self.is_valid(x, y):
            if self.board[y][x] and self.board[y][x].color == self.turn:
                self.selected = self.board[y][x]
            else:
                if self.selected_movables and (x, y) in self.selected_movables:
                    if self.promotionables and (x, y) in self.promotionables and (not self.board[y][x] or self.board[y][x].kind != "king"):
                        captured = None
                        if self.board[y][x]: captured = self.board[y][x]
                        previous_location = (self.selected.x, self.selected.y)
                        self.selected.move(x, y)

                        if self.selected.color: color = 6
                        else: color = 0
                        mx, my = pg.mouse.get_pos()
                        nx = (mx - self.real_xy(x))//(sq_size//2)
                        ny = (my - self.real_xy(y))//(sq_size//2)
                        if (nx, ny) == (0, 0):
                            self.board[y][x] = Queen(self.board, x, y, self.selected.player, self.imgs[color+4])
                            self.remove_from_dict(self.selected)
                            self.add_to_dict(self.board[y][x])
                        elif (nx, ny) == (1, 0):
                            self.board[y][x] = Knight(self.board, x, y, self.selected.player, self.imgs[color+1])
                            self.remove_from_dict(self.selected)
                            self.add_to_dict(self.board[y][x])
                        elif (nx, ny) == (0, 1):
                            self.board[y][x] = Rook(self.board, x, y, self.selected.player, self.imgs[color+2])
                            self.remove_from_dict(self.selected)
                            self.add_to_dict(self.board[y][x])
                        else:
                            self.board[y][x] = Bishop(self.board, x, y, self.selected.player, self.imgs[color+3])
                            self.remove_from_dict(self.selected)
                            self.add_to_dict(self.board[y][x])
                        
                        self.turn = not self.turn
                        self.log.append([previous_location, (x, y), captured, "promotion"])
                        self.add_board_log()
                    else:
                        captured = None
                        was_moved = True
                        if self.board[y][x]: captured = self.board[y][x]
                        previous_location = (self.selected.x, self.selected.y)
                        if not self.selected.is_moved:
                            was_moved = False
                        self.selected.move(x, y)
                        self.turn = not self.turn
                        self.log.append([previous_location, (x, y), captured, was_moved, "normal"])
                        self.add_board_log()
                elif (x, y) == self.en_passant:
                    previous_location = (self.selected.x, self.selected.y)
                    self.selected.move(x, y)
                    captured = self.board[y+self.selected.get_dis(1)][x]
                    self.board[captured.y][captured.x] = None
                    self.remove_from_dict(captured)
                    self.turn = not self.turn
                    self.log.append([previous_location, (x, y), captured, "en_passant"])
                    self.add_board_log()
                elif self.castleables and (x, y) in self.castleables:
                    # 퀸 사이드 캐슬링
                    if x == 2:
                        previous_location = (self.selected.x, self.selected.y, 0)
                        self.board[y][0].move(3, y)
                    # 킹 사이드 캐슬링
                    else:
                        previous_location = (self.selected.x, self.selected.y, 7)
                        self.board[y][7].move(5, y)
                    self.selected.move(x, y)
                    self.turn = not self.turn
                    self.log.append([previous_location, (x, y), "castling"])
                    self.add_board_log()
                self.initialize_variables()

        if not self.white_player.piece_dict["kings"]:
            self.winner = 1
            self.is_gameover = 1
        elif not self.black_player.piece_dict["kings"]:
            self.winner = 2
            self.is_gameover = 1
        else:
            self.check_checkmate()
            self.check_draw()

    def mouse_over(self, screen):
        x, y = self.get_xy(pg.mouse.get_pos())
        if self.is_valid(x, y):
            pg.draw.rect(self.temp_screen, grey, [self.real_xy(x), self.real_xy(y), sq_size, sq_size])
            screen.blit(self.temp_screen, (0, 0))

    def mouse_over_above_pieces(self, screen):
        x, y = self.get_xy(pg.mouse.get_pos())
        if self.is_valid(x, y):
            if self.promotionables and (x, y) in self.promotionables and (not self.board[y][x] or self.board[y][x].kind != "king"):
                mx, my = pg.mouse.get_pos()
                nx = (mx - self.real_xy(x))//(sq_size//2)
                ny = (my - self.real_xy(y))//(sq_size//2)
                pg.draw.rect(screen, purple, [self.real_xy(x)+sq_size*nx//2, self.real_xy(y)+sq_size*ny//2, sq_size//2, sq_size//2])

                imgs = []
                if self.selected.color: color = "white"
                else: color = "black"
                for piece in ["queen", "knight", "rook", "bishop"]:
                    imgs.append(pg.transform.scale(pg.image.load("Chess/images/"+color+"_"+piece+".png"), (sq_size//2, sq_size//2)))
                for i in range(2):
                    for j in range(2):
                        self.screen.blit(imgs[i*2+j], (self.real_xy(x)+sq_size*j//2, self.real_xy(y)+sq_size*i//2))

    def undo(self):
        if self.log:
            prev = self.log.pop()
            self.board_log.pop()
            self.fifty_move_log.pop()
            if prev[-1] == "normal":
                px, py = prev[0]
                cx, cy = prev[1]
                moved_piece = self.board[cy][cx]
                self.board[py][px] = moved_piece
                self.set_xy(px, py)
                if not prev[3]:
                    self.board[py][px].is_moved = False
                self.board[cy][cx] = prev[2]
                if prev[2]:
                    self.add_to_dict(prev[2])
                    self.set_xy(cx, cy)
            elif prev[-1] == "promotion":
                px, py = prev[0]
                cx, cy = prev[1]
                if self.board[cy][cx].color: color = 6
                else: color = 0
                self.board[py][px] = Pawn(self.board, px, py, self.board[cy][cx].player, self.imgs[color])
                self.add_to_dict(self.board[py][px])
                self.board[py][px].is_moved = True
                self.remove_from_dict(self.board[cy][cx])
                self.board[cy][cx] = prev[2]
                if prev[2]:
                    self.add_to_dict(prev[2])
                    self.set_xy(cx, cy)
            elif prev[-1] == "castling":
                kx, ky, rx = prev[0]
                cx, cy = prev[1]
                self.board[ky][kx] = self.board[cy][cx]
                self.board[cy][cx] = None
                self.set_xy(kx, ky)
                self.board[ky][kx].is_moved = False
                if rx == 0:
                    self.board[ky][rx] = self.board[ky][3]
                    self.board[ky][3] = None
                else:
                    self.board[ky][rx] = self.board[ky][5]
                    self.board[ky][5] = None
                self.set_xy(rx, ky)
                self.board[ky][rx].is_moved = False
            elif prev[-1] == "en_passant":
                px, py = prev[0]
                cx, cy = prev[1]
                moved_piece = self.board[cy][cx]
                self.board[py][px] = moved_piece
                self.set_xy(px, py)
                self.board[cy][cx] = None
                captured = prev[2]
                self.board[captured.y][captured.x] = captured
                self.add_to_dict(captured)

            self.turn = not self.turn
            self.initialize_variables()

    def check_event(self, screen):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click(screen, event.pos)
                elif event.button == 3:
                    self.undo()
            elif event.type == pg.QUIT:
                self.end_game()

    def add_board_log(self):
        count = 0
        board = []
        en_passant = False # 앙파상 가능한 상황은 3수 동형반복이 불가능하므로 흑백 구분을 하지 않음
        white_castling = False
        black_castling = False
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece:
                    if not en_passant and piece.kind == "pawn" and piece.is_en_passantable(self.log[-1]):
                        en_passant = True
                    if piece.kind == "king" and piece.is_castleable():
                        if piece.color:
                            white_castling = True
                        else:
                            black_castling = True
                    board.append(piece.kind)
                    count += 1
                else:
                    board.append("")
        self.board_log.append([count, board, not self.turn, en_passant, white_castling, black_castling])
        
    def restart(self, screen):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.is_gameover = False
            elif event.type == pg.QUIT:
                self.end_game()

    def print_message(self, screen):
        if self.is_gameover == 1:
            self.print_text(f"{['흑', '백'][self.winner-1]} 승리! 다시 시작하려면 아무 곳이나 우클릭하세요", white, [scr_size//2, scr_size-mg//2])
        elif self.is_gameover == 2:
            self.print_text(f"기물 부족 무승부. 다시 시작하려면 아무 곳이나 우클릭하세요", white, [scr_size//2, scr_size-mg//2])
        elif self.is_gameover == 3:
            self.print_text(f"3회 동형반복 무승부. 다시 시작하려면 아무 곳이나 우클릭하세요", white, [scr_size//2, scr_size-mg//2])
        elif self.is_gameover == 4:
            self.print_text(f"50수 무승부. 다시 시작하려면 아무 곳이나 우클릭하세요", white, [scr_size//2, scr_size-mg//2])
        elif self.is_gameover == 5:
            self.print_text(f"스테일메이트. 다시 시작하려면 아무 곳이나 우클릭하세요", white, [scr_size//2, scr_size-mg//2])
        elif self.is_gameover == 6:
            self.print_text(f"체크메이트! {['흑', '백'][self.winner-1]} 승리! 다시 시작하려면 아무 곳이나 우클릭하세요", white, [scr_size//2, scr_size-mg//2])

    def check_checkmate(self):
        if self.is_stalemate(checkmate=True):
            self.is_gameover = 6
            if self.turn: self.winner = 2
            else: self.winner = 1

    def check_draw(self):
        self.count_fifty_move()
        if self.is_impossibility_of_checkmate():
            self.is_gameover = 2
            return True
        elif self.is_threefold_repetition():
            self.is_gameover = 3
            return True
        elif self.is_fifty_move():
            self.is_gameover = 4
            return True
        elif self.is_stalemate():
            self.is_gameover = 5
        return False
    
    def is_impossibility_of_checkmate(self):
        players = [self.white_player, self.black_player]
        counts = []
        for player in players:
            count = ""
            for piece in piece_list:
                count += str(len(player.piece_dict[piece+"s"]))
            counts.append(count)

        if counts[0] == "000001" and counts[1] == "000001":
            return True
        elif (counts[0] == "000001" and counts[1] == "000101") or (counts[0] == "000101" and counts[1] == "000001"):
            return True
        elif (counts[0] == "000001" and counts[1] == "010001") or (counts[0] == "010001" and counts[1] == "000001"):
            return True
        elif counts[0] == "000101" and counts[1] == "000101":
            white_bishop = self.white_player.piece_dict["bishops"][0]
            black_bishop = self.black_player.piece_dict["bishops"][0]
            if white_bishop.x % 2 == white_bishop.y % 2 and black_bishop.x % 2 != black_bishop.y % 2:
                return True
            elif white_bishop.x % 2 != white_bishop.y % 2 and black_bishop.x % 2 == black_bishop.y % 2:
                return True
        return False

    def is_threefold_repetition(self):
        count = 0
        for log in self.board_log:
            if log == self.board_log[-1]:
                count += 1
        if count == 3:
            return True
        return False

    def count_fifty_move(self):
        if self.log and len(self.log) == len(self.fifty_move_log):
            prev = self.log[-1]
            if prev[-1] == "en_passant" or prev[-1] == "promotion" or prev[-1] == "normal" and (prev[2] or self.board[prev[1][1]][prev[1][0]].kind == "pawn"):
                self.fifty_move_log.append(0)
            else:
                self.fifty_move_log.append(self.fifty_move_log[-1]+1)

    def is_fifty_move(self):
        if len(self.fifty_move_log) >= 100 and self.fifty_move_log[-1] == 100:
            return True
        return False

    def is_stalemate(self, checkmate=False):
        if self.turn: player = self.white_player
        else: player = self.black_player
        king = player.piece_dict["kings"][0]
        # 1. 킹은 체크상태가 아니어야 함
        if checkmate:
            if not king.is_attacked(king.x, king.y):
                return False
        else:
            if king.is_attacked(king.x, king.y):
                return False
        # 2. 킹의 이동 가능한 모든 자리가 공격받는 상태라 킹이 이동할 수 없어야 함
        for x, y in king.get_movables():
            # is_attacked(x, y)가 각 기물들의 get_movables()에 (x, y)가 있는지 판단하기 때문에
            # (x, y)에 적 기물이 있다면, 적 기물의 get_movables()에 (x, y)가 포함되지 않음.
            # 그래서 임시로 (x, y)를 비우고 is_attacked(x, y)를 호출함.
            if self.board[y][x]:
                attacked = False
                piece = self.board[y][x]
                self.board[y][x] = None
                if king.is_attacked(x, y):
                    attacked = True
                self.board[y][x] = piece
                if not attacked:
                    return False
            else:
                if not king.is_attacked(x, y):
                    return False
        for bx in range(8):
            for by in range(8):
                piece = self.board[by][bx]
                if piece and piece.color == self.turn:
                    movables = piece.get_movables()
                    if movables:
                        for x, y in movables:
                            is_king_attacked = False
                            captured = None
                            was_moved = True
                            if self.board[y][x]: captured = self.board[y][x]
                            if not piece.is_moved:
                                was_moved = False
                            piece.move(x, y)
                            if king.is_attacked(king.x, king.y):
                                is_king_attacked = True
                            self.board[by][bx] = piece
                            self.set_xy(bx, by)
                            if not was_moved:
                                piece.is_moved = False
                            self.board[y][x] = captured
                            if captured:
                                self.add_to_dict(captured)
                            # 3. 어떤 수를 두어도 킹이 체크상태가 되어서 이동할 수 없어야 함
                            if not is_king_attacked:
                                return False
        return True

    def play_game(self, screen):
        while True:
            while not self.is_gameover:
                screen.fill(background_color)
                self.temp_screen.fill((0, 0, 0, 0))
                self.draw_board(screen)
                self.draw_selected(screen)
                self.check_event(screen)
                self.mouse_over(screen)
                self.draw_pieces(screen)
                self.mouse_over_above_pieces(screen)
                pg.display.flip()
                clock.tick(fps)

            while self.is_gameover:
                screen.fill(background_color)
                self.draw_board(screen)
                self.draw_pieces(screen)
                self.print_message(screen)
                self.restart(screen)
                pg.display.flip()
                clock.tick(fps)

            self.winner = 0
            self.turn = True
            self.initialize_variables()
            self.board = [[None for y in range(8)] for x in range(8)]
            self.log = []
            self.board_log = []
            self.fifty_move_log = [0]
            self.set_players()

        self.end_game()
    
    def end_game(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()