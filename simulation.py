import pygame
from grid import Grid
from ant import Ant

class Simulation:
    def __init__(self, grid, step_size):
        self.grid = grid #access all inside grid
        self.ants = [] #access all inside ants
        self.step_size = step_size

    def add_ant(self, x, y, col = (50, 30, 0)):
        if self.validate_move((x, y)):
            self.ants.append(Ant((x, y), col))
            return
        print(f'out of bounds: {x,y}')

    def validate_move(self, pos):
        newX = self.grid.xOff + pos[0]
        newY = self.grid.yOff + pos[1]
        return pygame.Rect.collidepoint(self.grid.rect, (newX, newY))
    
    def render_ants(self, screen):
        for ant in self.ants:
            ant.render(screen, self.grid.xOff, self.grid.yOff)

    def update_ants(self):
        for ant in self.ants:
            ant.move(self.step_size, pygame.Rect(0, 0, self.grid.size[0], self.grid.size[1]))