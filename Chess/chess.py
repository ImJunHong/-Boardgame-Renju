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

screen_size = 900
square_size = 100
margin = 50
color_list = ["black", "white"]
piece_list = ["pawn", "knight", "rook", "bishop", "queen", "king"]

fps = 60
clock = pg.time.Clock()

def main():
    pg.init()
    screen = pg.display.set_mode([screen_size, screen_size])
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
        self.selected = None
        self.selected_movables = None
        self.castleables = None
        self.promotionables = None
        self.en_passant = None
        self.board = [[None for y in range(8)] for x in range(8)]
        self.log = []
        self.font = pg.font.SysFont("새굴림", 14)
        self.imgs = self.load_images()
        self.set_players()
        self.play_game(screen)
    
    def load_images(self):
        imgs = []
        for color in color_list:
            for piece in piece_list:
                imgs.append(pg.transform.scale(pg.image.load("Chess/images/"+color+"_"+piece+".png"), (square_size, square_size)))
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

    def get_xy(self, pos):
        x, y = pos
        x = (x-margin)//square_size
        y = (y-margin)//square_size
        return x, y

    def get_original(self, x):
        return margin + x*square_size

    def set_xy(self, x, y):
        self.board[y][x].x = x
        self.board[y][x].y = y

    def is_valid(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        return False
    
    def draw_board(self, screen):
        pg.draw.rect(screen, white, [margin, margin, 8*square_size, 8*square_size])
        for i in range(8):
            for j in range(4):
                pg.draw.rect(screen, greyblue, [self.get_original((j*2+(i+1)%2)), self.get_original(i), square_size, square_size])
        bdr = 4
        pg.draw.rect(screen, black, [margin-bdr, margin-bdr, 8*square_size+bdr*2, 8*square_size+bdr*2], bdr)

    def draw_selected(self, screen):
        if self.selected:
            x = self.selected.x
            y = self.selected.y
            pg.draw.rect(screen, pink, [self.get_original(x), self.get_original(y), square_size, square_size])

            self.selected_movables = self.selected.get_movables()
            for mx, my in self.selected_movables:
                if self.board[my][mx] and self.board[my][mx].kind == "king":
                    pg.draw.rect(screen, yellow, [self.get_original(mx), self.get_original(my), square_size, square_size])
                else:
                    pg.draw.rect(screen, lightgreen, [self.get_original(mx), self.get_original(my), square_size, square_size])

            if self.selected.kind == "king":
                self.castleables = self.selected.is_castleable()
                if self.castleables:
                    for x, y in self.castleables:
                        pg.draw.rect(screen, lime, [self.get_original(x), self.get_original(y), square_size, square_size])
                        self.print_text("Castling", black, [self.get_original(x)+square_size//2, self.get_original(y)+square_size//2])
            elif self.selected.kind == "pawn":
                self.promotionables = self.selected.is_promotionable(self.selected_movables)
                if self.log:
                    self.en_passant = self.selected.is_en_passantable(self.log[-1])
                    if self.en_passant:
                        x, y = self.en_passant
                        pg.draw.rect(screen, lime, [self.get_original(x), self.get_original(y), square_size, square_size])
                        self.print_text("En Passant", black, [self.get_original(x)+square_size//2, self.get_original(y)+square_size//2])

    def draw_pieces(self, screen):
        for x in range(8):
            for y in range(8):
                if self.board[y][x]:
                    self.screen.blit(self.board[y][x].img, (self.get_original(x), self.get_original(y)))

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
                        nx = (mx - self.get_original(x))//(square_size//2)
                        ny = (my - self.get_original(y))//(square_size//2)
                        if (nx, ny) == (0, 0):
                            self.board[y][x] = Queen(self.board, x, y, self.selected.player, self.imgs[color+4])
                            self.selected.player.piece_dict["pawns"].remove(self.selected)
                            self.board[y][x].player.piece_dict["queens"].append(self.board[y][x])
                        elif (nx, ny) == (1, 0):
                            self.board[y][x] = Knight(self.board, x, y, self.selected.player, self.imgs[color+1])
                            self.selected.player.piece_dict["pawns"].remove(self.selected)
                            self.board[y][x].player.piece_dict["knights"].append(self.board[y][x])
                        elif (nx, ny) == (0, 1):
                            self.board[y][x] = Rook(self.board, x, y, self.selected.player, self.imgs[color+2])
                            self.selected.player.piece_dict["pawns"].remove(self.selected)
                            self.board[y][x].player.piece_dict["rooks"].append(self.board[y][x])
                        else:
                            self.board[y][x] = Bishop(self.board, x, y, self.selected.player, self.imgs[color+3])
                            self.selected.player.piece_dict["pawns"].remove(self.selected)
                            self.board[y][x].player.piece_dict["bishops"].append(self.board[y][x])
                        
                        self.turn = not self.turn
                        self.log.append([previous_location, (x, y), captured, "promotion"])
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
                elif (x, y) == self.en_passant:
                    previous_location = (self.selected.x, self.selected.y)
                    self.selected.move(x, y)
                    captured = self.board[y+self.selected.get_dis(1)][x]
                    self.board[captured.y][captured.x] = None
                    captured.player.piece_dict["pawns"].remove(captured)
                    self.turn = not self.turn
                    self.log.append([previous_location, (x, y), captured, "en_passant"])
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
                self.selected = None
                self.selected_movables = None
                self.castleables = None
                self.promotionables = None
                self.en_passant = None
                
        if not self.white_player.piece_dict["kings"]:
            self.winner = 1
            self.is_gameover = True
        elif not self.black_player.piece_dict["kings"]:
            self.winner = 2
            self.is_gameover = True

    def mouse_over(self, screen):
        x, y = self.get_xy(pg.mouse.get_pos())
        if self.is_valid(x, y):
            pg.draw.rect(self.temp_screen, grey, [self.get_original(x), self.get_original(y), square_size, square_size])
            screen.blit(self.temp_screen, (0, 0))

    def mouse_over_above_pieces(self, screen):
        x, y = self.get_xy(pg.mouse.get_pos())
        if self.is_valid(x, y):
            if self.promotionables and (x, y) in self.promotionables and (not self.board[y][x] or self.board[y][x].kind != "king"):
                mx, my = pg.mouse.get_pos()
                nx = (mx - self.get_original(x))//(square_size//2)
                ny = (my - self.get_original(y))//(square_size//2)
                pg.draw.rect(screen, purple, [self.get_original(x)+square_size*nx//2, self.get_original(y)+square_size*ny//2, square_size//2, square_size//2])

                imgs = []
                if self.selected.color: color = "white"
                else: color = "black"
                for piece in ["queen", "knight", "rook", "bishop"]:
                    imgs.append(pg.transform.scale(pg.image.load("Chess/images/"+color+"_"+piece+".png"), (square_size//2, square_size//2)))
                for i in range(2):
                    for j in range(2):
                        self.screen.blit(imgs[i*2+j], (self.get_original(x)+square_size*j//2, self.get_original(y)+square_size*i//2))

    def undo(self):
        if self.log:
            prev = self.log.pop()
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
                    prev[2].player.piece_dict[prev[2].kind+"s"].append(prev[2])
                    self.set_xy(cx, cy)
            elif prev[-1] == "promotion":
                px, py = prev[0]
                cx, cy = prev[1]
                if self.board[cy][cx].color: color = 6
                else: color = 0
                self.board[py][px] = Pawn(self.board, px, py, self.board[cy][cx].player, self.imgs[color])
                self.board[py][px].player.piece_dict["pawns"].append(self.board[py][px])
                self.board[py][px].is_moved = True
                self.board[cy][cx].player.piece_dict[self.board[cy][cx].kind+"s"].remove(self.board[cy][cx])
                self.board[cy][cx] = prev[2]
                if prev[2]:
                    prev[2].player.piece_dict[prev[2].kind+"s"].append(prev[2])
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
                captured.player.piece_dict[captured.kind+"s"].append(captured)

            self.turn = not self.turn
            self.selected = None
            self.selected_movables = None
            self.castleables = None
            self.en_passant = None

    def check_event(self, screen):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click(screen, event.pos)
                elif event.button == 3:
                    self.undo()
            elif event.type == pg.QUIT:
                self.end_game()

    def restart(self, screen):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.is_gameover = False
            elif event.type == pg.QUIT:
                self.end_game()
                
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
                self.print_text(f"{['흑', '백'][self.winner-1]} 승리! 다시 시작하려면 아무 곳이나 우클릭하세요", white, [screen_size//2, screen_size-margin//2])
                self.restart(screen)
                pg.display.flip()
                clock.tick(fps)

            self.winner = 0
            self.turn = True
            self.selected = None
            self.selected_movables = None
            self.castleables = None
            self.promotionables = None
            self.en_passant = None
            self.board = [[None for y in range(8)] for x in range(8)]
            self.log = []
            self.set_players()

        self.end_game()
    
    def end_game(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()