import pygame
from sprite import Sprite
from input import is_key_pressed

class Player(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.movement_speed = 4

    def update(self):
        dx, dy = 0, 0

        if is_key_pressed(pygame.K_w):
            dy -= 1
        if is_key_pressed(pygame.K_s):
            dy += 1
        if is_key_pressed(pygame.K_a):
            dx -= 1
        if is_key_pressed(pygame.K_d):
            dx += 1

        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length

        self.x += dx * self.movement_speed
        self.y += dy * self.movement_speed