import pygame
from sprite import Sprite
from input import is_key_pressed
from entity import active_objs
from physics import Body

movement_speed = 4

class Player:
    def __init__(self):
        active_objs.append(self)

    def update(self):
        body = self.entity.get(Body)

        dx, dy = 0, 0

        if is_key_pressed(pygame.K_w):
            dy -= 1
        if is_key_pressed(pygame.K_s):
            dy += 1
        if is_key_pressed(pygame.K_a):
            dx -= 1
        if is_key_pressed(pygame.K_d):
            dx += 1

        # Normalize to prevent diagonal speed boost
        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length

        dx *= movement_speed
        dy *= movement_speed

        # --- X AXIS ---
        previous_x = self.entity.x
        self.entity.x += dx
        if not body.is_position_valid():
            self.entity.x = previous_x

        # --- Y AXIS ---
        previous_y = self.entity.y
        self.entity.y += dy
        if not body.is_position_valid():
            self.entity.y = previous_y