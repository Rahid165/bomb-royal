import pygame
from math import ceil

map = None

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        global map

        map = self
        self.tile_kinds = tile_kinds
        file = open(map_file, "r")
        data = file.read()
        file.close()
        self.tiles = []
        for line in data.split("\n"):
            row = []
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)
        
        self.tile_size = tile_size
        self.height = len(self.tiles)
        self.width = len(self.tiles[0]) if self.tiles else 0
    
    def get_tile_index(self, px, py):
        tx = px // self.tile_size
        ty = py // self.tile_size

        if 0 <= ty < len(self.tiles) and 0 <= tx < len(self.tiles[ty]):
            return self.tiles[ty][tx]
        return None

    def is_solid_at(self, px, py):
        tile_index = self.get_tile_index(px, py)
        if tile_index is None:
            return True

        return self.tile_kinds[tile_index].is_solid
    
    def is_point_solid(self, x, y):
        x_tile = int(x/self.tile_size)
        y_tile = int(y/self.tile_size)
        if x_tile < 0 or \
            y_tile < 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return False
        tile = self.tiles[y_tile][x_tile]
        return self.tile_kinds[tile].is_solid


    def is_rect_solid(self, x, y, width, height):
        # Check the top left and middle (if bigger than tile size)
        x_checks = int(ceil(width/self.tile_size))
        y_checks = int(ceil(height/self.tile_size))
        for yi in range(y_checks):
            for xi in range(x_checks):
                x = xi*self.tile_size + x
                y = yi*self.tile_size + y
                if self.is_point_solid(x, y):
                    return True
        if self.is_point_solid(x + width, y):
            return True
        if self.is_point_solid(x, y + height):
            return True
        if self.is_point_solid(x + width, y + height):
            return True
        return False

    def rect_collides(self, rect):
        return (
            self.is_solid_at(rect.left, rect.top) or
            self.is_solid_at(rect.right - 1, rect.top) or
            self.is_solid_at(rect.left, rect.bottom - 1) or
            self.is_solid_at(rect.right - 1, rect.bottom - 1)
        )

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)