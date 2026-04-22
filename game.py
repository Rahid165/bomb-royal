import pygame
import sys
import input
from player import Player
from sprite import sprites
from map import TileKind, Map

pygame.init()

width, height = 1280, 768
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("RPG")

clear_color = (30, 30, 30)

running = True
clock = pygame.time.Clock()
player = Player("images/player.png", 0, 0)

tile_kinds = [
    TileKind("dirt", "images/dirt.png", False),
    TileKind("gre_brick_wall", "images/grey-brick-wall.png", True),
    TileKind("tree", "images/tree.png", True)
]
map = Map("maps/start.map", tile_kinds, 64)

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
    map.draw(screen)
    for s in sprites:
        s.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()