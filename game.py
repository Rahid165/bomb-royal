import pygame
import sys
import input
from player import Player
from sprite import sprites

pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("RPG")

clear_color = (30, 30, 30)

running = True

player = Player("images/player.png", 0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.discard(event.key)

    player.update()

    screen.fill(clear_color)
    for s in sprites:
        s.draw(screen)

    pygame.display.flip()
    pygame.time.delay(17)

pygame.quit()
sys.exit()