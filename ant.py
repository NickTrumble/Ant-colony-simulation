#class containing ants
import numpy as np
import pygame

class Ant:

    def __init__(self, box, centre, cell_size):
        self.col = (50, 30, 0)
        self.body = 6
        self.head = 5
        self.tail = 8

        self.last_dir = (0, 1)

        self.cell_size = cell_size
        (self.x, self.y) = (9, 7) #local position (centre grid)
        self.theta = 0 #facing direction
        (self.width, self.height) = box
        (self.xOff, self.yOff) = (centre[0] - self.width // 2, centre[1] - self.height // 2)

    def find_move(self):
        possible = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if self.last_dir == (0, 1): #down
            dir = 0
        elif self.last_dir == (1, 0): # right
            dir = 1
        elif self.last_dir == (0, -1): #up
            dir = 2
        elif self.last_dir == (-1, 0): # left
            dir = 3
        dir += np.random.randint(-1, 1)
        print(dir)
        
        return possible[(dir+ 4) % 4]

    def render(self, screen):
        headCenter = (
            (self.head + self.body) * np.cos(self.theta) + self.x * self.cell_size + self.xOff, 
            (self.head + self.body) * np.sin(self.theta) + self.y * self.cell_size + self.yOff
            )
        bodyCenter = (
            self.x * self.cell_size + self.xOff, 
            self.y * self.cell_size + self.yOff
            )
        tailCenter = (
                - (self.tail + self.body) * np.cos(self.theta) + self.x * self.cell_size + self.xOff, 
                - (self.tail + self.body) * np.sin(self.theta) + self.y * self.cell_size + self.yOff)
        
        pygame.draw.circle(screen, self.col, headCenter, self.head) #head
        pygame.draw.circle(screen, self.col, bodyCenter, self.body) #body
        pygame.draw.circle(screen, self.col, tailCenter, self.tail) #tail

    def rotate(self, dir):
        if dir == (0, 1): #down
            self.theta = np.pi / 2
        elif dir == (1, 0): # right
            self.theta = 0
        elif dir == (0, -1): #up
            self.theta = 3 * np.pi / 2
        elif dir == (-1, 0): # left
            self.theta =  np.pi

    def move(self):
        (x, y) = self.find_move()
        while not self.validate_move((x, y)):
            (x, y) = self.find_move()
        self.last_dir = (x, y)
        print (x, y)
        self.rotate((x, y))
        self.x += x
        self.y += y

    def validate_move(self, dir):
        newX = self.x + dir[0]
        newY = self.y + dir[1]
        if newX > self.width // self.cell_size or newX < 0:
            print(newX)
            return False #out of bounds
        if newY > self.height // self.cell_size or newY < 0:
            print(newY)
            return False
        return True