import pygame

class Grid:
    def __init__(self, xOff, yOff, width, height):
        self.xOff = xOff
        self.yOff = yOff
        self.size = (width, height)

        self.rect = pygame.Rect(xOff, yOff, width, height)

    