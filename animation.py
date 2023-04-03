import pygame
import sys
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (50, 50, 50)
NUM_CIRCLES = 10

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Complex Animation")

# Generate circle colors and frequency/amplitude pairs
circle_colors = [tuple(np.random.randint(50, 255, 3)) for _ in range(NUM_CIRCLES)]
circle_params = [(np.random.uniform(0.5, 3), np.random.uniform(0.1, 0.4)) for _ in range(NUM_CIRCLES)]

# Main game loop
clock = pygame.time.Clock()
running = True
angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Update the animation
    angle += 1
    if angle >= 360:
        angle = 0

    # Draw multiple circles moving along sinusoidal paths with different frequencies and amplitudes
    for i, (color, (freq, amp)) in enumerate(zip(circle_colors, circle_params)):
        x = int(WIDTH / 2 + math.cos(math.radians(angle * freq)) * WIDTH * amp)
        y = int(HEIGHT / 2 + math.sin(math.radians(angle * freq)) * HEIGHT * amp)
        pygame.draw.circle(screen, color, (x, y), 20)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
