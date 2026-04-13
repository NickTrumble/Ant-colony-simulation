import numpy as np
import pygame
from simulation import Simulation
from grid import Grid

#colours
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
BROWN = (50, 30, 0)
GREEN = (0, 80, 0)
RED = (100, 0, 0)

(width, height) = (800, 600)
offset = 0.1 #in percent

screen = pygame.display.set_mode((width, height))
background = GREEN

pygame.init()

grid = Grid(width * offset, height * offset, width * (1 - 2 * offset), height * (1 - 2 * offset))
def draw_outline():
    pygame.draw.rect(screen, BLACK, grid.rect, 1)


font = pygame.font.SysFont('Ariel', 24)
def write_title(i):
    img = font.render(f'Step: {i}', True, WHITE, background)
    screen.blit(img, (width // 2 - img.get_width() // 2, 20))


def main():
    running = True
    counter = 0
    while running:
        counter += 1
        screen.fill(background)
        draw_outline()
        write_title(counter)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    
        sim.update_ants()
        sim.render_objects(screen)

        pygame.display.flip()
        pygame.time.wait(1)
            

sim = Simulation(grid, 3)
for i in range(50):
    sim.add_ant()

main()
