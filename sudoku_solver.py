import pygame as pg
import random
import csv
import numpy as np

pg.init()
width = 540
height = 540 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
screen = pg.display.set_mode((width,height))
fps = 30
clock = pg.time.Clock()

def draw_grid(surface, spacing=60, color=white):
    for i in range(surface.get_width()):
        if i % 3 == 0:
            pg.draw.line(surface, color, (i*spacing, 0), (i*spacing, surface.get_height()), 5)
        else:
            pg.draw.line(surface, color, (i*spacing, 0), (i*spacing, surface.get_height()))
    for i in range(surface.get_height()):
        if i % 3 == 0:
            pg.draw.line(surface, color, (0, i*spacing), (surface.get_width(), i*spacing), 5)
        else:
            pg.draw.line(surface, color, (0, i*spacing), (surface.get_width(), i*spacing))

class Cell():
    size = 60
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.index = (self.row,self.col)
        self.x = self.col * self.size
        self.y = self.row * self.size
        self.pos = (self.x, self.y)
        self.image = pg.Surface((self.size,self.size))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.num = 0
    
    def draw(self):
        if self.num:
            self.image.fill(black)
            font = pg.font.SysFont('arial', 50)
            text = font.render(str(self.num), True, red)
            self.image.blit(text, (20,0))
        else:
            self.image.fill(black)
        
class Board():
    def __init__(self):
        self.cells = {}
        self.width = width
        self.height = height
        self.generate_cells()
        self.grid = self.setup()
    
    def generate_cells(self):
        for i in range(9):
            for j in range(9):
                self.cells[(i,j)] = Cell(i,j)
                
    def set_cells(self):
        for i in range(9):
            for j in range(9):
                self.cells[(i,j)].num = self.grid[i][j]
    def draw(self, screen):
        for cell in self.cells.values():
            cell.draw()
            screen.blit(cell.image, cell.pos)
            draw_grid(screen)
            
    def setup(self):
        choice = input('Would you like to manually enter the grid or use a file? Enter y to use a file: ')
        if choice == 'y':
            datafile = open('grid.csv', 'r')
            grid = np.genfromtxt(datafile, delimiter=',')
            grid = grid.astype(int)
            print(grid)
            return grid 
        else:
            running = True
            row = None
            col = None
            grid  = np.array([[0 for i in range(9)] for j in range(9)])
            while running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_s:
                            running = False
                        if row != None:
                            if event.key == pg.K_1:
                                grid[row][col] = 1
                            if event.key == pg.K_2:
                                grid[row][col] = 2
                            if event.key == pg.K_3:
                                grid[row][col] = 3
                            if event.key == pg.K_4:
                                grid[row][col] = 4
                            if event.key == pg.K_5:
                                grid[row][col] = 5
                            if event.key == pg.K_6:
                                grid[row][col] = 6
                            if event.key == pg.K_7:
                                grid[row][col] = 7
                            if event.key == pg.K_8:
                                grid[row][col] = 8
                            if event.key == pg.K_9:
                                grid[row][col] = 9
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                        for cell in self.cells.values():
                            if cell.rect.collidepoint(pos):
                                row = cell.row
                                col = cell.col
                    for i in range(9):
                        for j in range(9):
                            self.cells[(i,j)].num = grid[i][j]
                    self.draw(screen)
                    pg.display.flip()
            print(grid)
            return grid
    
    def isSafe(self, row, col, num):
   
        # Check if we find the same num
        # in the similar row , we
        # return false
        for x in range(9):
            if self.grid[row][x] == num:
                return False
 
        # Check if we find the same num in
        # the similar column , we
        # return false
        for x in range(9):
            if self.grid[x][col] == num:
                return False
 
        # Check if we find the same num in
        # the particular 3*3 matrix,
        # we return false
        startRow = row - row % 3
        startCol = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + startRow][j + startCol] == num:
                    return False
        return True
 
    def solve(self):
        # self.set_cells()
        # self.draw(screen)
        # pg.display.flip()
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for n in range(1,10):
                        if self.isSafe(y, x, n):
                            self.grid[y][x] = n
                            self.solve()
                            self.grid[y][x] = 0
                    return
        print(self.grid)
        self.set_cells()
        
def main():
    running = True
    b = Board()
    b.solve()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill(black)
        # Insert update code
        b.draw(screen)
        pg.display.flip()
        clock.tick(30)

main()
pg.quit()