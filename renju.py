import pygame as pg
import sys
from rule import Rule

background_color = (204, 153,   0)
black            = (  0,   0,   0)
white            = (255, 255, 255)

screen_size = [500, 500]
cell_size = 30
stone_size = 13
margin = 40
stones = [[0 for y in range(15)] for x in range(15)] # 빈 칸 0, 흑 1, 백 2
log = []
rule = Rule(stones, log)

fps = 60
done = False
clock = pg.time.Clock()

def main():
    pg.init()
    screen = pg.display.set_mode(screen_size)
    pg.display.set_caption("Renju")
    game = Game(screen)

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.is_gameover = False
        self.font = pg.font.SysFont("새굴림", 14)
        self.play_game(screen)

    def print_text(self, msg, color, pos):
        if color == 0: color = white
        elif color == 1: color = black
        textSurface = self.font.render(msg, True, color, None)
        textRect = textSurface.get_rect()
        textRect.center = pos
        self.screen.blit(textSurface, textRect)
    
    def draw_board(self, screen):
        for i in range(15):
            pg.draw.aaline(screen, black, [margin, margin+cell_size*i], [500-margin, margin+cell_size*i])
            pg.draw.aaline(screen, black, [margin+cell_size*i, margin], [margin+cell_size*i, 500-margin])
        
        pg.draw.circle(screen, black, [130, 130], 3)
        pg.draw.circle(screen, black, [370, 130], 3)
        pg.draw.circle(screen, black, [130, 370], 3)
        pg.draw.circle(screen, black, [370, 370], 3)
        pg.draw.circle(screen, black, [250, 250], 3)
        
    def draw_stones(self, screen):
        for count in range(len(log)):
            x, y = log[count]

            if stones[y][x] == 1:
                pg.draw.circle(screen, black, [margin+cell_size*x, margin+cell_size*y], stone_size)
            elif stones[y][x] == 2:
                pg.draw.circle(screen, white, [margin+cell_size*x, margin+cell_size*y], stone_size)

            self.print_text(str(count+1), count%2, (margin+cell_size*x, margin+cell_size*y))

    def click(self, screen, pos):
        x, y = pos
        board_x = (x-margin+cell_size//2)//30
        board_y = (y-margin+cell_size//2)//30
        if board_x >= 0 and board_y >=0 and stones[board_y][board_x] == 0:
            stones[board_y][board_x] = len(log)%2+1
            log.append((board_x, board_y))

    def undo(self):
        if log:
            x, y = log.pop()
            stones[y][x] = 0

    def check_event(self, screen):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click(screen, event.pos)
                elif event.button == 3:
                    self.undo()
                self.check_rule()
            elif event.type == pg.QUIT:
                self.end_game()

    def check_rule(self):
        for x in range(15):
            for y in range(15):
                for direction in range(4):
                    pass

    def play_game(self, screen):
        while not done:
            screen.fill(background_color)
            self.draw_board(screen)
            self.check_event(screen)
            self.draw_stones(screen)
            pg.display.flip()
            clock.tick(fps)

        self.end_game()
    
    def end_game(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()