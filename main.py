import pygame
import random
import math
import tile_map

pygame.init()

TILE_SIZE = 25
ROW_COUNT = 40
COLUMN_COUNT = 60
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

ENEMY_TIMER = 3.1
ENEMY_STOP_RANGE = 360
ENEMY_ATTACK_RANGE = 400

BOMB_TIMER = 1.5
BOMB_SPEED = 8
BOMB_DAMAGE = 20

bombs = []
enemies = []
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


def check_collision_circle(bx, by, tx, ty, bomb_radius, target_radius):
    dx = tx - bx
    dy = ty - by
    dist = math.sqrt(dx**2 + dy**2)

    return dist < (bomb_radius + target_radius)


def check_collison_tile(bx, by, radius, tiles):
    bomb_rect = pygame.Rect(bx - radius, by - radius, radius*2, radius*2)
    
    for tile in tiles:
        if bomb_rect.colliderect(tile):
            return True
        
    return False


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

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        x = random.randint(0, WIDTH)
        y = 0 + 20
    elif side == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT - 20
    elif side == "left":
        x = 0 + 20
        y = random.randint(0, HEIGHT)
    elif side == "right":
        x = WIDTH - 20
        y = random.randint(0, HEIGHT)

    enemies.append([x, y, BOMB_TIMER * 60, 1000])


def shoot_bomb(ex, ey, px, py):
    dx = px - ex
    dy = py - ey

    dist = math.sqrt(dx*dx + dy*dy)
    if dist == 0:
        return

    dx /= dist
    dy /= dist

    vx = dx * BOMB_SPEED
    vy = dy * BOMB_SPEED

    bombs.append([ex, ey, vx, vy, False, 0])


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
    tiles.clear()
    collision_tiles.clear()

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
                

def move_random_towards(ex, ey, px, py, speed):
    dirc_vec = pygame.math.Vector2(px - ex, py - ey)

    if dirc_vec.length == 0:
        return ex, ey
    
    dirc_vec = dirc_vec.normalize()

    random_vec = pygame.math.Vector2(random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3))

    move_vec = dirc_vec + random_vec

    if move_vec.length() > 0:
        move_vec = move_vec.normalize()

    ex += move_vec.x * speed
    ey += move_vec.y * speed

    return ex, ey


def distance(ex, ey, px, py):
    dx = px - ex
    dy = py - ey

    dist = math.sqrt(dx**2 + dy**2)

    return dist


def reset_game():
    x = WIDTH // 2
    y = HEIGHT // 2
    health = MAX_HEALTH

    bombs = []
    enemies = []

    enemy_timer = 180
    shoot_timer = 0

    return x, y, health, bombs, enemies, enemy_timer, shoot_timer


def main():
    x, y, health, bombs, enemies, enemy_timer, shoot_timer = reset_game()

    running = True

    create_map()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
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

        current_time = pygame.time.get_ticks()

        #Draw Tiles
        for tile_type, rect in tiles:
            if tile_type == 1:
                pygame.draw.rect(screen, GREY, rect)

        enemy_timer += 1
        if enemy_timer > ENEMY_TIMER * 60:
            spawn_enemy()
            enemy_timer = 0

        #Enemy Movement
        for e in enemies:
            ex, ey = e[0], e[1]

            dist = distance(ex, ey, x, y)

            if dist > ENEMY_STOP_RANGE:
                # move toward player
                e[0], e[1] = move_random_towards(ex, ey, x, y, 2)
            else:
                # stop (or idle)
                pass

        # enemies
        for e in enemies:
            pygame.draw.circle(screen, GREEN, (int(e[0]), int(e[1])), 20)
            e[3] = distance(e[0], e[1], x, y)
            e[2] -= 1
            if e[2] == 0:
                if e[3] < ENEMY_ATTACK_RANGE:
                    shoot_bomb(e[0], e[1], x, y)
                e[2] = BOMB_TIMER * 60

        # bombs
        for b in bombs:
            bx, by, vx, vy, exploding, timer = b

            if not exploding:
                pygame.draw.circle(screen, RED, (int(bx), int(by)), 8)
            else:
                # explosion grows
                radius = 8 + (15 - timer)
                pygame.draw.circle(screen, (255, 150, 0), (int(bx), int(by)), radius)

        for b in bombs[:]:  # copy list (important)
            bx, by, vx, vy, exploding, timer = b

            if not exploding:
                # move
                bx += vx
                by += vy

                # check collision
                if check_collision_circle(bx, by, x, y, 8, PLAYER_RADIUS):
                    b[4] = True  # start explosion
                    b[5] = 15    # frames of explosion
                    health = do_damage(health, BOMB_DAMAGE)

                elif check_collison_tile(bx, by, 8, collision_tiles):
                    b[4] = True
                    b[5] = 15

            else:
                # explosion countdown
                b[5] -= 2
                if b[5] <= 0:
                    bombs.remove(b)
                    continue

            b[0], b[1] = bx, by

        if health <= 0:
            pygame.time.delay(500)  # small pause (optional)
            x, y, health, bombs, enemies, enemy_timer, shoot_timer = reset_game()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()