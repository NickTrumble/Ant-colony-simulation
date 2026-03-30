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
        sim.render_ants(screen)

        pygame.display.flip()
        pygame.time.wait(100)
            

sim = Simulation(grid, 3)
for i in range(20):
    sim.add_ant(300, 200)

main()


#old locals - delete
# (width, height) = (800, 600)
# cells_wide = 50
# cell_size = width // cells_wide 
# box = (width - 2 * (cell_size), height - 2 * cell_size)
# centre = (width // 2, height // 2)

#old systme - not encapsulated
# ants = []
# ants.append(Ant(box, centre, cell_size))

# #getting rid of grid - delete
# def draw_grid():
#     for i in range(cell_size, width - cell_size, cell_size):
#         for j in range(cell_size, height - cell_size, cell_size):
#             rect = pygame.Rect(i, j, cell_size, cell_size)
#             pygame.draw.rect(screen, WHITE, rect, 1)

# #old cell system - redo
# def generate_food():
#     (x, y) = (np.random.randint(0, cells_wide), np.random.randint(0, cells_wide * 3 / 4))
#     apple = pygame.Rect(x * cell_size, y * cell_size,  cell_size, cell_size)
#     pygame.draw.rect(screen, RED, apple, 1)