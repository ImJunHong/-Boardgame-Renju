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

screen_size = 900
square_size = 100
margin = 50
colors = ["black", "white"]
pieces = ["pawn", "knight", "rook", "bishop", "queen", "king"]

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
        self.color = color # 0 백, 1 흑
        self.piece_dict = {"pawns":[], "knights":[], "rooks":[], "bishops":[], "queens":[], "king":[]}
        self.set_pieces(imgs)

    def set_pieces(self, imgs):
        nums = [0, 1, 7, 6]
        for i in range(8):
            self.piece_dict["pawns"].append(Pawn(self.board, i, nums[self.color*2+1], imgs[self.color*6]))
        for i in range(2):
            self.piece_dict["knights"].append(Knight(self.board, 5*i+1, nums[self.color*2], imgs[self.color*6+1]))
            self.piece_dict["rooks"].append(Knight(self.board, 7*i, nums[self.color*2], imgs[self.color*6+2]))
            self.piece_dict["bishops"].append(Bishop(self.board, 3*i+2, nums[self.color*2], imgs[self.color*6+3]))
        self.piece_dict["queens"].append(Queen(self.board, 3, nums[self.color*2], imgs[self.color*6+4]))
        self.piece_dict["king"].append(King(self.board, 4, nums[self.color*2], imgs[self.color*6+5]))

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.temp_screen = screen.convert_alpha()
        self.is_gameover = False
        self.winner = 0
        self.selected = None
        self.board = [[None for y in range(8)] for x in range(8)]
        self.font = pg.font.SysFont("새굴림", 14)
        self.imgs = self.load_images()
        self.set_players()
        self.play_game(screen)
    
    def load_images(self):
        imgs = []
        for color in colors:
            for piece in pieces:
                imgs.append(pg.transform.scale(pg.image.load("Chess/images/"+color+"_"+piece+".png"), (square_size, square_size)))
        return imgs

    def set_players(self):
        self.white_player = Player(self.board, 0, self.imgs)
        self.black_player = Player(self.board, 1, self.imgs)
        self.players = [self.white_player, self.black_player]
        for line in self.board:
            print(line)

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
            x, y = self.selected
            pg.draw.rect(screen, pink, [margin+square_size*x, margin+square_size*y, square_size, square_size])


    def draw_pieces(self, screen):
        for x in range(8):
            for y in range(8):
                if self.board[y][x]:
                    self.screen.blit(self.board[y][x].img, (margin+square_size*x, margin+square_size*y))

    def click(self, screen, pos):
        x, y = self.get_xy(pos)
        if self.is_valid(x, y) and self.board[y][x]:
            self.selected = (x, y)

    def mouse_over(self, screen):
        x, y = self.get_xy(pg.mouse.get_pos())
        if self.is_valid(x, y):
            pg.draw.rect(self.temp_screen, grey, [margin+square_size*x, margin+square_size*y, square_size, square_size])
            screen.blit(self.temp_screen, (0, 0))

    def undo(self):
        pass

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
                self.print_text(f"{['흑', '백'][self.winner-1]} 승리! 다시 시작하려면 아무 곳이나 우클릭하세요", white, [screen_size//2, screen_size-margin//2])
                self.restart(screen)
                pg.display.flip()
                clock.tick(fps)

        self.end_game()
    
    def end_game(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()