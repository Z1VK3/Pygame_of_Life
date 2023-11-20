# Python version = 3.8.5
from settings import *
import random
import sys
from builtins import range
import pygame

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE + 100))
pygame.display.set_caption("Pygame of Life")
clock = pygame.time.Clock()

pygame.font.init()
header_font = pygame.font.SysFont('Comic Sans MS', 30)
text_font = pygame.font.SysFont('Comic Sans MS', 12)


# Functions
def initialize_grid(width, height):
    """ Creating a grid of size width*height and initializing all cells to off(0)"""
    grid_list = [[0] * width for _ in range(height)]
    return grid_list


def randomize_entire_grid(grid1):
    """ Randomly setting all cells in the grid to either off(0) or on(1) """
    for x in range(HEIGHT):
        for y in range(WIDTH):
            grid1[x][y] = random.randrange(2)
    return grid1


def create_glider_gun(grid1):
    """ Adding a glider-gun """
    # Used pattern from:
    # https://humberto.io/blog/exploring-pygame-4-game-of-life/

    for x in range(WIDTH):
        for y in range(HEIGHT):
            grid1[x][y] = 0
    grid1[20][30] = 1
    grid1[21][28] = grid1[21][30] = 1
    grid1[22][18] = grid1[22][19] = grid1[22][26] = grid1[22][27] = grid1[22][40] = grid1[22][41] = 1
    grid1[23][17] = grid1[23][21] = grid1[23][26] = grid1[23][27] = grid1[23][40] = grid1[23][41] = 1
    grid1[24][6] = grid1[24][7] = grid1[24][16] = grid1[24][22] = grid1[24][26] = grid1[24][27] = 1
    grid1[25][6] = grid1[25][7] = grid1[25][16] = grid1[25][20] = grid1[25][22] = grid1[25][23] = 1
    grid1[25][28] = grid1[25][30] = 1
    grid1[26][16] = grid1[26][22] = grid1[26][30] = 1
    grid1[27][17] = grid1[27][21] = 1
    grid1[28][18] = grid1[28][19] = 1
    return grid1


def add_random_glider(grid1):
    """ Adding a glider to the grid in a random unoccupied position """
    x = random.randrange(1, HEIGHT - 4)
    y = random.randrange(1, WIDTH - 4)

    if grid1[x][y] == grid1[x + 1][y + 1] == grid1[x + 2][y - 1] == grid1[x + 2][y] == \
            grid1[x + 2][y + 1] == 0:
        grid1[x][y] = 1
        grid1[x + 1][y + 1] = 1
        grid1[x + 2][y - 1] = grid1[x + 2][y] = grid1[x + 2][y + 1] = 1
    else:
        add_random_glider(grid1)
    return grid1


def check_adjacent_cells(y, x, grid_state):
    """ Checking the number of adjacent alive cell to a given cell and returning that number"""
    alive = 0
    adjacent_cells = [[y - 1, x - 1], [y - 1, x], [y - 1, x + 1], [y, x + 1], [y + 1, x + 1], [y + 1, x],
                      [y + 1, x - 1], [y, x - 1]]
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
        else:  # survival
            new_cell_state = 1
    else:
        if number_of_adjacent_alive == 3:  # birth
            new_cell_state = 1
        else:
            new_cell_state = 0
    return new_cell_state


# Initializing the grid with all cell set to 0
grid = initialize_grid(WIDTH, HEIGHT)
create_glider_gun(grid)

# Game loop
running = True
reset = False

while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Pressing 'ESC' to close the window
                running = False
            if event.key == pygame.K_SPACE:  # Pressing 'Space-Bar' to clear the grid
                reset = True
            if event.key == pygame.K_1:  # Pressing '1' will add a glider to the grid at a random location
                # to clear the grid
                add_random_glider(grid)
            if event.key == pygame.K_2:  # Pressing '2' will randomize the entire grid
                randomize_entire_grid(grid)
            if event.key == pygame.K_3:  # Pressing '3' will clear the grid and add a glider-gun
                create_glider_gun(grid)

    screen.fill(BLACK)

    # Initialized grid for the next generation
    new_gen_grid = initialize_grid(WIDTH, HEIGHT)
    # Clearing the grid if space-bar is pressed
    if reset:
        grid = new_gen_grid
        reset = False
    # Going through the grid, drawing cells that are alive and populating the grid for the next generation
    # according to the game's rules
    else:
        for row_number, current_row in enumerate(grid):
            for cell_number, cell_value in enumerate(current_row):
                pygame.draw.rect(screen, BLACK, (cell_number * CELL_SIZE, row_number * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if cell_value == 1:
                    pygame.draw.rect(screen, GREEN, (cell_number * CELL_SIZE + BORDER, row_number * CELL_SIZE - BORDER,
                                                     CELL_SIZE - BORDER, CELL_SIZE - BORDER))
                fate = check_cell_fate(grid[row_number][cell_number],
                                       check_adjacent_cells(row_number, cell_number, grid))
                new_gen_grid[row_number][cell_number] = fate

        grid = new_gen_grid

    # Guide at the bottom of the screen
    pygame.draw.rect(screen, pygame.Color('grey40'), (0, HEIGHT * CELL_SIZE + 1, WIDTH * CELL_SIZE, 100))
    text_surface1 = text_font.render('1 - adds a glider to the grid at a random location', True, (0, 0, 0))
    screen.blit(text_surface1, (25, HEIGHT * CELL_SIZE + 10))
    text_surface2 = text_font.render('2 - randomize the entire grid', True, (0, 0, 0))
    screen.blit(text_surface2, (25, HEIGHT * CELL_SIZE + 30))
    text_surface3 = text_font.render('3 - clears the grid and adds a glider-gun', True, (0, 0, 0))
    screen.blit(text_surface3, (25, HEIGHT * CELL_SIZE + 50))
    text_surface3 = text_font.render('Spacebar - Clears the entire grid', True, (0, 0, 0))
    screen.blit(text_surface3, (25, HEIGHT * CELL_SIZE + 70))
    pygame.display.flip()

pygame.quit()
