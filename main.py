import pygame
import random
import math
import tile_map

pygame.init()

TILE_SIZE = 25
ROW_COUNT = 24
COLUMN_COUNT = 32
WIDTH, HEIGHT = TILE_SIZE * COLUMN_COUNT, TILE_SIZE * ROW_COUNT
GAME_MAP = tile_map.GAME_MAP1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Circle with Health Bar")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

PLAYER_RADIUS = 25
PLAYER_SPEED = 8

MAX_HEALTH = 100

BOMB_SPEED = 7
BOMB_DAMAGE = 20

bombs = []
background_tiles = []
tiles = []
collision_tiles = []

def handle_movement(keys, x, y, speed):
    direction = pygame.math.Vector2(0, 0)

    if keys[pygame.K_a]:
        direction.x -= 1
    if keys[pygame.K_d]:
        direction.x += 1
    if keys[pygame.K_w]:
        direction.y -= 1
    if keys[pygame.K_s]:
        direction.y += 1

    if direction.length() > 0:
        direction = direction.normalize()

    x += direction.x * speed
    y += direction.y * speed

    return x, y


def move_with_collision(x, y, dx, dy, radius, collision_tiles):
    # convert circle → rect hitbox
    player_rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)

    # --- X movement ---
    player_rect.x += dx
    for tile in collision_tiles:
        if player_rect.colliderect(tile):
            if dx > 0:  # moving right
                player_rect.right = tile.left
            elif dx < 0:  # moving left
                player_rect.left = tile.right

    # --- Y movement ---
    player_rect.y += dy
    for tile in collision_tiles:
        if player_rect.colliderect(tile):
            if dy > 0:  # moving down
                player_rect.bottom = tile.top
            elif dy < 0:  # moving up
                player_rect.top = tile.bottom

    return player_rect.centerx, player_rect.centery


def clamp_player(x, y, radius, width, height):
    if x - radius < 0:
        x = radius
    if x + radius > width:
        x = width - radius
    if y - radius < 0:
        y = radius
    if y + radius > height:
        y = height - radius
    return x, y


def draw_player(surface, x, y, radius):
    pygame.draw.circle(surface, WHITE, (x, y), radius)


def draw_bomb(surface, x, y, color, radius):
    pygame.draw.circle(surface, color, (x, y), radius)


def spawn_bomb(et):
    if et == 120:
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        spawn_time = pygame.time.get_ticks()
        bombs.append([x, y, spawn_time, True])


def draw_health_bar(surface, health, max_health, x, y, width, height):
    health_ratio = health / max_health
    current_width = width * health_ratio

    pygame.draw.rect(surface, RED, (x, y, width, height))
    pygame.draw.rect(surface, GREEN, (x, y, current_width, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)


def do_damage(health, damage):
    health = health - damage
    return health


def create_map():
    for row in range(len(GAME_MAP)):
        for column in range(len(GAME_MAP[row])):
            map_code = GAME_MAP[row][column]
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            if map_code == 0:
                continue
            
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            tiles.append((map_code, rect))

            if map_code == 1:
                collision_tiles.append(rect)
                

def main():
    x, y = WIDTH // 2, HEIGHT // 2
    health = MAX_HEALTH
    running = True
    enemy_timer = 0

    create_map()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        #x, y = handle_movement(keys, x, y, PLAYER_SPEED)
        dx, dy = 0, 0

        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1

        # normalize
        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2) ** 0.5
            dx /= length
            dy /= length

        dx *= PLAYER_SPEED
        dy *= PLAYER_SPEED

        x, y = move_with_collision(x, y, dx, dy, PLAYER_RADIUS, collision_tiles)
        x, y = clamp_player(x, y, PLAYER_RADIUS, WIDTH, HEIGHT)

        if health < 0:
            health = 0

        screen.fill(BLACK)
        draw_player(screen, x, y, PLAYER_RADIUS)
        draw_health_bar(screen, health, MAX_HEALTH, 20, 20, 200, 20)

        spawn_bomb(enemy_timer)

        current_time = pygame.time.get_ticks()

        #Draw Tiles
        for tile_type, rect in tiles:
            if tile_type == 1:
                pygame.draw.rect(screen, GREY, rect)

        for c in bombs:
            bx, by, spawn_time, active = c

            if active != True:
                bombs.remove(c)
                health = do_damage(health, BOMB_DAMAGE)

            c[0], c[1] = bx, by

        enemy_timer += 1

        if enemy_timer > 120:
            enemy_timer = 0

        for c in bombs:
            bx, by, spawn_time, active = c

            if current_time - spawn_time > 1000:
                color = RED
            else:
                color = (255, 255, 0)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()