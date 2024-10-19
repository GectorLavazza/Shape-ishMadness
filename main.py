import pygame
import time
from particles import *

from enemies import *
from player import Player


def set_screen(size):
    pygame.display.set_caption('Shapish Madness')
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, size[0], size[1])

    return screen, size, screen_rect


pygame.init()
clock = pygame.time.Clock()
fps = 60
screen, size, screen_rect = set_screen((800, 800))

last_time = time.time()

running = True

particles_g = pygame.sprite.Group()
bullets_g = pygame.sprite.Group()
enemies_g = pygame.sprite.Group()

player_g = pygame.sprite.Group()
player = Player(bullets_g, particles_g, player_g)

enemy_spawn = EnemySpawn(enemies_g, particles_g, bullets_g)

shooting = False
shooting_cooldown = 0

while running:

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_e:
                player.hold_mode = not player.hold_mode

            if event.key == pygame.K_F1:
                if fps == 120:
                    fps = 60
                elif fps == 60:
                    fps = 10
                elif fps == 10:
                    fps = 120

            if event.key == pygame.K_w:
                player.dy = -1
            if event.key == pygame.K_s:
                player.dy = 1
            if event.key == pygame.K_a:
                player.dx = -1
            if event.key == pygame.K_d:
                player.dx = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.dy = 0
            if event.key == pygame.K_s:
                player.dy = 0
            if event.key == pygame.K_a:
                player.dx = 0
            if event.key == pygame.K_d:
                player.dx = 0

        if player.hold_mode:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.hold = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    player.hold = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot(mouse_pos)

    if player.hold_mode:
        if player.hold:
            player.hold_cooldown += dt
            if player.hold_cooldown >= 10:
                player.shoot(mouse_pos)
                player.hold_cooldown = 0

    screen.fill(pygame.Color('#0f380f'))

    particles_g.update(screen_rect, dt, fps)
    player_g.update(screen_rect, dt)
    bullets_g.update(screen_rect, dt)
    enemies_g.update(screen, screen_rect, (player.rect.x, player.rect.y), dt)
    enemy_spawn.update(dt)

    bullets_g.draw(screen)
    player_g.draw(screen)
    particles_g.draw(screen)
    enemies_g.draw(screen)


    pygame.display.update()
    clock.tick(fps)

pygame.quit()
