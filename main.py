import pygame
import sys
import input
from player import Player
from sprite import sprites, Sprite
from map import TileKind, Map
from entity import Entity, active_objs
from physics import Body

pygame.init()

width, height = 1280, 768
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("RPG")

clear_color = (30, 30, 30)

running = True
clock = pygame.time.Clock()

player = Entity(Player(), Sprite("images/player.png"), Body(35, 95-20, 26, 20), x=96, y=96)

tile_kinds = [
    TileKind("dirt", "images/dirt2.png", False),
    TileKind("gre_brick_wall", "images/grey-brick-wall.png", True),
    TileKind("water", "images/water.png", True)
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

    for a in active_objs:
        a.update()

    screen.fill(clear_color)
    map.draw(screen)
    for s in sprites:
        s.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()