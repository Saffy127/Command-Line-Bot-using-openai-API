import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
BACKGROUND_COLOR = (50, 50, 50)
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)

# Grid dimensions
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life with Garden of Eden")

# Initialize the grid with Garden of Eden configuration
eden_pattern = """
0000111011100
0111000101011
1010101010100
1101101010110
0101010101010
0110101010110
1010101010100
1101000101100
"""

eden_pattern = [list(map(int, row.strip())) for row in eden_pattern.strip().split('\n')]
eden_height, eden_width = len(eden_pattern), len(eden_pattern[0])

grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
grid[:eden_height, :eden_width] = eden_pattern

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, ALIVE_COLOR, rect)
            else:
                pygame.draw.rect(screen, DEAD_COLOR, rect)
            pygame.draw.rect(screen, BACKGROUND_COLOR, rect, 1)

def update_grid():
    global grid
    new_grid = grid.copy()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            alive_neighbors = np.sum(grid[y - 1:y + 2, x - 1:x + 2]) - grid[y][x]

            # Cell rules
            if grid[y][x] == 1 and (alive_neighbors < 2 or alive_neighbors > 3):
                new_grid[y][x] = 0
            elif grid[y][x] == 0 and alive_neighbors == 3:
                new_grid[y][x] = 1

    grid = new_grid

# Main game loop
clock = pygame.time.Clock()
running = True
generation = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle cell state on mouse click
            x, y = event.pos
            grid[y // CELL_SIZE][x // CELL_SIZE] = 1 - grid[y // CELL_SIZE][x // CELL_SIZE]

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    draw_grid()

    # Update the grid
    update_grid()
    generation += 1

    # Add random perturbation every 100 generations
    if generation % 100 == 0:
        random_y, random_x = np.random.randint(0, GRID_HEIGHT), np.random.randint(0, GRID_WIDTH)
        grid[random_y][random_x] = 1 - grid[random_y][random_x]

    # Update the display
    pygame.display.flip()
    clock.tick(10)

# Quit the game
pygame.quit()
sys.exit()
