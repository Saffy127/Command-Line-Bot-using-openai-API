import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1600, 900
CELL_SIZE = 10
BACKGROUND_COLOR = (50, 50, 50)
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)

# Grid dimensions
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life with Turing Tumble Configuration")

# Initialize the grid with the Turing Tumble configuration
turing_tumble = [
    "0000000000000000000000000000000110000",
    "0000000000000000000000000000001001000",
    "0000000000000000000000000110001001000",
    "0000000000000000000000001001011000100",
    "0000000000000110000000001000001000100",
    "0000000000001001000000001001011000100",
    "0000000000110001000000001001001000100",
    "0000000001001011000000000110001000100",
    "0000000001000001000110000000101000100",
    "0000000001001011001001000000110000100",
    "0000000001001001000000000000000000100",
    "0000000000110001000000000000000000100",
    "0000000000000101000000000000000000100",
    "0000000000000110000000000000000000100",
]

turing_tumble = [list(map(int, row.strip())) for row in turing_tumble]
turing_height, turing_width = len(turing_tumble), len(turing_tumble[0])

grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
grid[:turing_height, :turing_width] = turing_tumble

# Rest of the code remains unchanged

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")


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

    # Update the display
    pygame.display.flip()
    clock.tick(10)

# Quit the game
pygame.quit()
sys.exit()