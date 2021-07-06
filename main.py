# Python version = 3.8.5

from builtins import range
import pygame

# Variables
WIDTH = 50
HEIGHT = 50
FPS = 5
CELL_SIZE = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
pygame.display.set_caption("Pygame of Life")
clock = pygame.time.Clock()

# Functions


def initialize_grid(width, height):
    """ Creating a grid of size width*height and initializing all cells to off(0)"""
    grid_list = [[0] * width for _ in range(height)]
    return grid_list


def check_adjacent_cells(y, x, grid_state):
    """ Checking the number of adjacent alive cell to a given cell and returning that number"""
    alive = 0
    adjacent_cells = [[y-1, x-1], [y-1, x], [y-1, x+1], [y, x+1], [y+1, x+1], [y+1, x], [y+1, x-1], [y, x-1]]
    for j in adjacent_cells:
        if (0 <= j[0] < len(grid_state)) and (0 <= j[1] < len(grid_state[0])):
            if grid_state[j[0]][j[1]] == 1:
                alive += 1
    return alive


def check_cell_fate(current_cell_state, number_of_adjacent_alive):
    """ Deciding the state of a cell in the upcoming generation according to the game's rules"""
    if current_cell_state == 1:
        if number_of_adjacent_alive <= 1 or number_of_adjacent_alive >= 4:  # isolation and overcrowding
            new_cell_state = 0
        else:   # survival
            new_cell_state = 1
    else:
        if number_of_adjacent_alive == 3:   # birth
            new_cell_state = 1
        else:
            new_cell_state = 0
    return new_cell_state


# Initializing the grid with all cell set to 0
grid = initialize_grid(WIDTH, HEIGHT)

# Adding a Glider
grid[2][2] = 1
grid[3][3] = 1
grid[4][1] = grid[4][2] = grid[4][3] = 1

# Game loop
running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Initialized grid for the next generation
    new_gen_grid = initialize_grid(WIDTH, HEIGHT)

    # Going through the grid, drawing cells that are alive and populating the grid for the next generation according to the game's rules
    for row_number, current_row in enumerate(grid):
        for cell_number, cell_value in enumerate(current_row):
            if cell_value == 1:
                pygame.draw.rect(screen, GREEN, (cell_number * CELL_SIZE, row_number * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            fate = check_cell_fate(grid[row_number][cell_number], check_adjacent_cells(row_number, cell_number, grid))
            new_gen_grid[row_number][cell_number] = fate

    grid = new_gen_grid
    pygame.display.flip()

pygame.quit()
