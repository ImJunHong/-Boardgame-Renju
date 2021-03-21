import pygame as pg
import sys
import ctypes
from rule import *

background_color = (204, 153,   0)
black            = (  0,   0,   0)
white            = (255, 255, 255)
red              = (255,   0,   0)

cell_size = 30
margin = 50
scr_size = cell_size * (MAX - 1) + 2 * margin
stone_size = 13

fps = 60
clock = pg.time.Clock()

def main():
    pg.init()
    screen = pg.display.set_mode([scr_size, scr_size])
    pg.display.set_caption("Go")
    game = Game(screen)

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.is_gameover = False
        self.font = pg.font.SysFont("새굴림", 14)
        self.winner = 0
        self.play_game(screen)

    def print_text(self, msg, color, pos):
        if color == 0: color = white
        elif color == 1: color = black
        textSurface = self.font.render(msg, True, color, None)
        textRect = textSurface.get_rect()
        textRect.center = pos
        self.screen.blit(textSurface, textRect)
    
    def draw_board(self, screen):
        for i in range(MAX):
            pg.draw.aaline(screen, black, [margin, margin+cell_size*i], [scr_size-margin, margin+cell_size*i])
            pg.draw.aaline(screen, black, [margin+cell_size*i, margin], [margin+cell_size*i, scr_size-margin])
        
        pg.draw.circle(screen, black, [margin+cell_size*3, margin+cell_size*3], 3)
        pg.draw.circle(screen, black, [margin+cell_size*(MAX-4), margin+cell_size*3], 3)
        pg.draw.circle(screen, black, [margin+cell_size*3, margin+cell_size*(MAX-4)], 3)
        pg.draw.circle(screen, black, [margin+cell_size*(MAX-4), margin+cell_size*(MAX-4)], 3)
        pg.draw.circle(screen, black, [margin+cell_size*((MAX-1)//2), margin+cell_size*((MAX-1)//2)], 3)

        pg.draw.rect(screen, black, [0, 0, margin, margin//2])
        self.print_text("계가", white, [margin//2, margin//4])

        if self.is_gameover:
            self.print_text(f"점수 [ 흑: {self.scores[BLACK]}집, 백: {self.scores[WHITE]}집 ]", black, [scr_size//2, margin//2])
        else:
            self.print_text(f"따낸 돌 [ 흑: {self.scores[BLACK]}, 백: {self.scores[WHITE]} ]", black, [scr_size//2, margin//2])
        
    def draw_stones(self, screen):
        for count in range(len(self.log)):
            x = self.log[count][0]
            y = self.log[count][1]

            if self.stones[y][x] == BLACK:
                pg.draw.circle(screen, black, [margin+cell_size*x, margin+cell_size*y], stone_size)
            elif self.stones[y][x] == WHITE:
                pg.draw.circle(screen, white, [margin+cell_size*x, margin+cell_size*y], stone_size)
            
            if self.stones[y][x] != EMPTY:
                self.print_text(str(count+1), count%2, (margin+cell_size*x, margin+cell_size*y))

    def click(self, screen, pos):
        x, y = pos
        board_x = (x-margin+cell_size//2)//cell_size
        board_y = (y-margin+cell_size//2)//cell_size
        color = len(self.log)%2+1
        if is_valid(self.stones, board_x, board_y, color, self.board_log):
            self.stones[board_y][board_x] = color
            captured = capture(self.stones, color)
            if captured:
                self.log.append((board_x, board_y, captured))
                self.scores[color] += len(captured)
            else:
                self.log.append((board_x, board_y))
            self.board_log.append(to_string(self.stones))
        else:
            if x <= margin and y <= margin//2:
                territory = is_countable(self.stones)
                if territory:
                    self.scores[BLACK] += territory[BLACK]
                    self.scores[WHITE] += territory[WHITE] + KOMI
                    if self.scores[BLACK] > self.scores[WHITE]:
                        self.winner = BLACK
                    else:
                        self.winner = WHITE
                    self.is_gameover = True
                else:
                    ctypes.windll.user32.MessageBoxW(0, "아직 계가할 수 없습니다.", "계가 불가능", 0)

    def undo(self):
        if self.log:
            self.board_log.pop()
            if len(self.log[-1]) == 2:
                x, y = self.log.pop()
                self.stones[y][x] = 0
            elif len(self.log[-1]) == 3:
                x, y, captured = self.log.pop()
                self.stones[y][x] = 0
                color = (len(self.log)+1)%2+1
                self.scores[get_enemy(color)] -= len(captured)
                for cx, cy in captured:
                    self.stones[cy][cx] = color

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
            self.stones = [[0 for y in range(MAX)] for x in range(MAX)]
            self.log = []
            self.board_log = []
            self.scores = [None, 0, 0]
            while not self.is_gameover:
                screen.fill(background_color)
                self.draw_board(screen)
                self.check_event(screen)
                self.draw_stones(screen)
                pg.display.flip()
                clock.tick(fps)
            while self.is_gameover:
                screen.fill(background_color)
                self.draw_board(screen)
                self.draw_stones(screen)
                self.print_text(f"{['흑', '백'][self.winner-1]} {abs(self.scores[1]-self.scores[2])}집 승! 다시 시작하려면 아무 곳이나 우클릭하세요", black, [scr_size//2, scr_size-margin//2])
                self.restart(screen)
                pg.display.flip()
                clock.tick(fps)

        self.end_game()
    
    def end_game(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()