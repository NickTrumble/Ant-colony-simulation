import pygame
import numpy as np

class Grid:
    def __init__(self, xOff, yOff, width, height):
        self.xOff = xOff
        self.yOff = yOff
        self.size = (int(width), int(height))

        self.rect = pygame.Rect(xOff, yOff, width, height)

        self.aPheremone = np.zeros(self.size) #without food
        self.bPheremone = np.zeros(self.size) #with food

        self.foodmap = np.zeros(self.size) #1 for food, 0 for none
        self.fill_foodmap()

        self.nest = (self.size[0] // 2, self.size[1] // 2)

    def fill_foodmap(self, amount=5):
        for _ in range(amount):
            x = np.random.randint(1, self.size[0] - 1)
            y = np.random.randint(1, self.size[1] - 1)

            self.foodmap[x, y] = np.random.uniform(5, 10)

    