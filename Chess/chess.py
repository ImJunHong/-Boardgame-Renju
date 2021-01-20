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
yellow           = (250, 225,  20)

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
        self.players = [self.white_player, self.black_player]

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

    def is_valid(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True
        return False
    
    def draw_board(self, screen):
        pg.draw.rect(screen, white, [margin, margin, 8*square_size, 8*square_size])
        for i in range(8):
            for j in range(4):
                pg.draw.rect(screen, greyblue, [margin+square_size*(j*2+(i+1)%2), margin+square_size*i, square_size, square_size])
        bdr = 4
        pg.draw.rect(screen, black, [margin-bdr, margin-bdr, 8*square_size+bdr*2, 8*square_size+bdr*2], bdr)

    def draw_selected(self, screen):
        if self.selected:
            x = self.selected.x
            y = self.selected.y
            pg.draw.rect(screen, pink, [margin+square_size*x, margin+square_size*y, square_size, square_size])
            self.selected_movables = self.selected.get_movables()
            for mx, my in self.selected_movables:
                if self.board[my][mx] and self.board[my][mx].kind == "king":
                    pg.draw.rect(screen, yellow, [margin+square_size*mx, margin+square_size*my, square_size, square_size])
                else:
                    pg.draw.rect(screen, lightgreen, [margin+square_size*mx, margin+square_size*my, square_size, square_size])

    def draw_pieces(self, screen):
        for x in range(8):
            for y in range(8):
                if self.board[y][x]:
                    self.screen.blit(self.board[y][x].img, (margin+square_size*x, margin+square_size*y))

    def click(self, screen, pos):
        x, y = self.get_xy(pos)
        if self.is_valid(x, y):
            if self.selected_movables and (x, y) in self.selected_movables:
                catched = None
                was_moved = True
                if self.board[y][x]: catched = self.board[y][x]
                previous_location = (self.selected.x, self.selected.y)
                if not self.selected.is_moved:
                    was_moved = False
                self.selected.move(x, y)
                self.selected = None
                self.selected_movables = None
                self.turn = not self.turn
                self.log.append([previous_location, (x, y), catched, was_moved])
                
            elif self.board[y][x] and self.board[y][x].color == self.turn:
                self.selected = self.board[y][x]

        if not self.white_player.piece_dict["kings"]:
            self.winner = 1
            self.is_gameover = True
        elif not self.black_player.piece_dict["kings"]:
            self.winner = 2
            self.is_gameover = True

    def mouse_over(self, screen):
        x, y = self.get_xy(pg.mouse.get_pos())
        if self.is_valid(x, y):
            pg.draw.rect(self.temp_screen, grey, [margin+square_size*x, margin+square_size*y, square_size, square_size])
            screen.blit(self.temp_screen, (0, 0))

    def undo(self):
        if self.log:
            prev = self.log.pop()
            px, py = prev[0]
            cx, cy = prev[1]
            moved_piece = self.board[cy][cx]
            self.board[py][px] = moved_piece
            self.board[py][px].x = px
            self.board[py][px].y = py
            if not prev[3]:
                self.board[py][px].is_moved = False
            self.board[cy][cx] = prev[2]
            if prev[2]:
                self.board[cy][cx].player.piece_dict[self.board[cy][cx].kind+"s"].append(self.board[cy][cx])
                self.board[cy][cx].x = cx
                self.board[cy][cx].y = cy
            self.turn = not self.turn
            self.selected = []
            self.selected_movables = []

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
            self.board = [[None for y in range(8)] for x in range(8)]
            self.log = []
            self.set_players()

        self.end_game()
    
    def end_game(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()