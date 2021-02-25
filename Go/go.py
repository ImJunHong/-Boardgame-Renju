import pygame as pg
import sys
from rule import Rule

background_color = (204, 153,   0)
black            = (  0,   0,   0)
white            = (255, 255, 255)
red              = (255,   0,   0)

cell_size = 30
margin = 40
cell_amount = 19
screen_size = cell_size * (cell_amount - 1) + 2 * margin
stone_size = 13

fps = 60
clock = pg.time.Clock()

def main():
    pg.init()
    screen = pg.display.set_mode([screen_size, screen_size])
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
        for i in range(cell_amount):
            pg.draw.aaline(screen, black, [margin, margin+cell_size*i], [screen_size-margin, margin+cell_size*i])
            pg.draw.aaline(screen, black, [margin+cell_size*i, margin], [margin+cell_size*i, screen_size-margin])
        
        pg.draw.circle(screen, black, [margin+cell_size*3, margin+cell_size*3], 3)
        pg.draw.circle(screen, black, [margin+cell_size*15, margin+cell_size*3], 3)
        pg.draw.circle(screen, black, [margin+cell_size*3, margin+cell_size*15], 3)
        pg.draw.circle(screen, black, [margin+cell_size*15, margin+cell_size*15], 3)
        pg.draw.circle(screen, black, [margin+cell_size*9, margin+cell_size*9], 3)
        
    def draw_stones(self, screen):
        for count in range(len(self.log)):
            x, y = self.log[count]

            if self.stones[y][x] == 1:
                pg.draw.circle(screen, black, [margin+cell_size*x, margin+cell_size*y], stone_size)
            elif self.stones[y][x] == 2:
                pg.draw.circle(screen, white, [margin+cell_size*x, margin+cell_size*y], stone_size)

            self.print_text(str(count+1), count%2, (margin+cell_size*x, margin+cell_size*y))

    def click(self, screen, pos):
        x, y = pos
        board_x = (x-margin+cell_size//2)//cell_size
        board_y = (y-margin+cell_size//2)//cell_size
        color = len(self.log)%2+1
        if Rule.is_valid(board_x, board_y) and self.stones[board_y][board_x] == 0:
            self.stones[board_y][board_x] = color
            self.log.append((board_x, board_y))

    def undo(self):
        if self.log:
            x, y = self.log.pop()
            self.stones[y][x] = 0

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
            self.stones = [[0 for y in range(cell_amount)] for x in range(cell_amount)]
            self.log = []
            self.rule = Rule(self.stones, self.log)
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
                self.print_text(f"{['흑', '백'][self.winner-1]} 승리! 다시 시작하려면 아무 곳이나 우클릭하세요", black, [screen_size//2, screen_size-margin//2])
                self.restart(screen)
                pg.display.flip()
                clock.tick(fps)

        self.end_game()
    
    def end_game(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()