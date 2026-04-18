import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Circle with Health Bar")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

PLAYER_RADIUS = 25
PLAYER_SPEED = 8

MAX_HEALTH = 100

bombs = []

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


def move_towards(bx, by, px, py, speed):
    dx = px - bx
    dy = py - by

    dist = math.sqrt(dx*dx + dy*dy)

    if dist <= 12.5:
        return bx, by, False

    dx /= dist
    dy /= dist

    bx += dx * speed
    by += dy * speed

    return bx, by, True


def draw_health_bar(surface, health, max_health, x, y, width, height):
    health_ratio = health / max_health
    current_width = width * health_ratio

    pygame.draw.rect(surface, RED, (x, y, width, height))
    pygame.draw.rect(surface, GREEN, (x, y, current_width, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)


def main():
    x, y = WIDTH // 2, HEIGHT // 2
    health = MAX_HEALTH
    running = True
    enemy_timer = 0

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        x, y = handle_movement(keys, x, y, PLAYER_SPEED)
        x, y = clamp_player(x, y, PLAYER_RADIUS, WIDTH, HEIGHT)

        if health < 0:
            health = 0

        screen.fill(BLACK)
        draw_player(screen, x, y, PLAYER_RADIUS)
        draw_health_bar(screen, health, MAX_HEALTH, 20, 20, 200, 20)

        spawn_bomb(enemy_timer)

        current_time = pygame.time.get_ticks()

        for c in bombs:
            bx, by, spawn_time, active = c

            if current_time - spawn_time > 1000:
                bx, by, active = move_towards(bx, by, x, y, 5)

            if active != True:
                bombs.remove(c)

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

            draw_bomb(screen, int(bx), int(by), color, 10)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()