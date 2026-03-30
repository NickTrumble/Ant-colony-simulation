#class containing ants
import numpy as np
import pygame

class Ant:

    def __init__(self, pos, col = (50, 30, 0)):
        #individual ant stuff - keep
        self.col = col
        self.sf = 1
        self.body = 3 * self.sf
        self.head = 4 * self.sf
        self.tail = 5 * self.sf
        

        (self.x, self.y) = pos
        self.theta = 0

    def move(self, step_size, bounds):
        (newX, newY) = self.next_location(step_size)
        #approach 1
        while not pygame.Rect.collidepoint(bounds, (newX, newY)):
            (newX, newY) = self.next_location(step_size)
        #approach 2
        #clip x and y inside boundary then will work
        # if not pygame.Rect.collidepoint(bounds, (newX, newY)):
        #     self.theta = 2 * np.pi - self.theta
        #     (newX, newY) = self.next_location(step_size)

        self.x = newX
        self.y = newY

    def next_location(self, step_size):
        self.pathfind_random()
        newX = self.x + step_size * np.cos(self.theta)
        newY = self.y + step_size * np.sin(self.theta)
        return (newX, newY)

    def pathfind_random(self):
        newTheta = self.theta + np.random.rand() - 0.5
        self.theta = (newTheta + 2 * np.pi) % (2 * np.pi)
        return

    def render(self, screen, xOff, yOff):
        headCenter = (
            (self.head + self.body) * np.cos(self.theta) + self.x + xOff, 
            (self.head + self.body) * np.sin(self.theta) + self.y + yOff
            )
        bodyCenter = (
            self.x + xOff, 
            self.y + yOff
            )
        tailCenter = (
                - (self.tail + self.body) * np.cos(self.theta) + self.x + xOff, 
                - (self.tail + self.body) * np.sin(self.theta) + self.y + yOff
                )
        
        pygame.draw.circle(screen, self.col, headCenter, self.head) #head
        pygame.draw.circle(screen, self.col, bodyCenter, self.body) #body
        pygame.draw.circle(screen, self.col, tailCenter, self.tail) #tail

    #old cell stuff, but usefull - redo
    # def validate_move(self, dir):
    #     newX = self.x + dir[0]
    #     newY = self.y + dir[1]
    #     if newX > self.width // self.cell_size or newX < 0:
    #         print(newX)
    #         return False #out of bounds
    #     if newY > self.height // self.cell_size or newY < 0:
    #         print(newY)
    #         return False
    #     return True