import pygame
import numpy as np
from ant import Ant

class Simulation:
    def __init__(self, grid, step_size):
        self.grid = grid #access all inside grid
        self.ants = [] #access all inside ants
        self.step_size = step_size
        self.rate = 0.2

    def add_ant(self,col = (50, 30, 0)):
        x, y = self.grid.nest
        if self.validate_move((x, y)):
            self.ants.append(Ant((x, y), col))
            return
        print(f'out of bounds: {x,y}')

    def validate_move(self, pos):
        newX = self.grid.xOff + pos[0]
        newY = self.grid.yOff + pos[1]
        return pygame.Rect.collidepoint(self.grid.rect, (newX, newY))
    
    def render_objects(self, screen):
        self.render_food(screen)
        self.render_pheremones(screen)
        self.render_nest(screen)
        self.render_ants(screen)

    def render_ants(self, screen):
        for ant in self.ants:
            ant.render(screen, self.grid.xOff, self.grid.yOff)

    def render_pheremones(self, screen):
        offset = (self.grid.xOff, self.grid.yOff)
        aPheremones = np.argwhere(self.grid.aPheremone > 0.01)
        bPheremones = np.argwhere(self.grid.bPheremone > 0.01)

        for i,j in aPheremones:
            intensity = int(np.clip(50 + 125 * self.grid.aPheremone[i, j] ** .7, 0, 255))
            pygame.draw.circle(screen, (0, 0, intensity), (i + offset[0], j + offset[1]), 2)
        for i, j in bPheremones:
            intensity = int(np.clip(50 + 125 * self.grid.bPheremone[i, j] ** .7, 0, 255))
            pygame.draw.circle(screen, (intensity, 0, 0), (i + offset[0], j + offset[1]), 2)

    def render_food(self, screen):
        food_indicies = np.argwhere(self.grid.foodmap)
        offset = (self.grid.xOff, self.grid.yOff)

        for i, j in food_indicies:
            intensity = (0, np.clip(self.grid.foodmap[i, j] * 50, 0, 255),40)
            pygame.draw.circle(screen, intensity, (i + offset[0], j + offset[1]), 5)

    def render_nest(self, screen):
        nest = (self.grid.nest[0] + self.grid.xOff, self.grid.nest[1] + self.grid.yOff)
        intensity = (100, 200, 50)
        pygame.draw.circle(screen, intensity, nest, 8)

    def update_ants(self):
        for ant in self.ants:
            ant.move(self.step_size, pygame.Rect(0, 0, self.grid.size[0], self.grid.size[1]), 
                     self.grid.foodmap, self.grid.nest, self.grid.aPheremone, self.grid.bPheremone)
            self.update_pheremones(ant)
        self.decrease_all_pheremones()
        
    def update_pheremones(self, ant):
        if ant.hasFood:
            self.grid.bPheremone[int(ant.x), int(ant.y)] += 0.4
        else:
            self.grid.aPheremone[int(ant.x), int(ant.y)] += 0.4
        
    def decrease_all_pheremones(self):
        self.grid.aPheremone = np.maximum(0, self.grid.aPheremone * .98)
        self.grid.bPheremone = np.maximum(0, self.grid.bPheremone * .98)

        self.grid.aPheremone[self.grid.aPheremone < 0.01] = 0
        self.grid.bPheremone[self.grid.bPheremone < 0.01] = 0

        self.grid.aPheremone = self.diffuse(self.grid.aPheremone, self.rate)
        self.grid.bPheremone = self.diffuse(self.grid.bPheremone, self.rate)

    def diffuse(self, pheromone, rate):
        copy = pheromone.copy()
        copy[1:-1, 1:-1] = (
            (1 - rate) * pheromone[1:-1, 1:-1] + 
            rate * (
                copy[1:-1, 1:-1] +
                copy[2:, 1:-1] +
                copy[:-2, 1:-1] +
                copy[1:-1, 2:] +
                copy[1:-1, :-2]
            ) / 5
        )

        copy[0, :] = 0
        copy[-1, :] = 0
        copy[:, 0] = 0
        copy[:, -1] = 0

        return copy