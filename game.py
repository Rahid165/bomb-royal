import pygame
import sys

pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("RPG")

clear_color = (30, 30, 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(clear_color)

    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()