import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image)
            loaded[image] = self.image
        sprites.append(self)

    def delete(self):
            sprites.remove(self)

    def draw(self, screen):
            screen.blit(self.image, (self.entity.x, self.entity.y))