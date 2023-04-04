import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
BACKGROUND_COLOR = (50, 50, 50)
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)

# Grid dimensions
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Initialize the grid
grid = np.random.choice([0, 1], (GRID_HEIGHT, GRID_WIDTH), p=[0.8, 0.2])

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    draw_grid()

    # Update the grid
    update_grid()

    # Update the display
    pygame.display.flip()
    clock.tick(10)

# Quit the game
pygame.quit()
sys.exit()
