import pygame
import random
from itertools import *

from particles import create_particles, generate_particles
from sprites import Sprite
from load_image import load_image

from settings import *
from items import *
from player import create_bullet, Bullet, create_enemy_bullet


class Triangle(Sprite):
    def __init__(self, pos, particles_g, bullet_g, items_g, player, *group):
        super().__init__(*group)
        self.image = load_image('triangle')
        self.name = 'triangle'
        self.rect = self.image.get_rect()

        self.particles_g = particles_g
        self.bullet_g = bullet_g
        self.player = player
        self.items_g = items_g

        self.rect.center = pos

        self.elapsed_time = 0

        self.quotient = (5 + self.player.score // 50 -
                         3 * self.player.score // 200 -
                         3 * self.player.score // 1000 -
                         3 * self.player.score // 2000 -
                         2 * self.player.score // 5000 -
                         1 * self.player.score // 10000) / 10
        if self.quotient > 1:
            self.quotient = 1

        self.max_speed = int(random.choices(range(4, 9),
                                            weights=(1, 2, 3, 2, 1), k=1)[0] *
                             self.quotient)
        if self.max_speed < 4:
            self.max_speed = 4

        self.health = 2
        self.max_health = 2
        self.damage = 1
        self.score_weight = 5
        self.dx = 0
        self.dy = 0

        self.damage_timer = 0

        self.hitbox = pygame.Rect(0, 0, 30, 30)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)

        self.acceleration = 0.7  # How quickly the enemy accelerates
        self.deceleration = 0.3  # How quickly the enemy decelerates
        self.velocity = pygame.Vector2(0, 0)  # Current velocity
        self.recovering = False  # Track if the enemy is recovering after the hit

    def update(self, screen, screen_rect, target_pos, dt):
        self.move(target_pos, dt)
        self.bullet_check()
        self.draw_health_bar(screen)
        self.player_check()

        # Handle damage cooldown and recovery
        if self.damage_timer < 120:
            self.damage_timer += dt
            self.recovering = True
        else:
            self.recovering = False  # Stop recovering when cooldown is done

    def move(self, target_pos, dt):
        direction = pygame.Vector2(target_pos) - pygame.Vector2(
            self.rect.center)

        if direction.length() > 0:
            direction = direction.normalize()

            # If recovering (after hitting the player), decelerate
            if self.recovering:
                self.velocity.x -= self.velocity.x * self.deceleration * 0.5 * dt
                self.velocity.y -= self.velocity.y * self.deceleration * 0.5 * dt
            else:
                # Normal acceleration towards the target
                self.velocity.x += direction.x * self.acceleration * dt
                self.velocity.y += direction.y * self.acceleration * dt
        else:
            # Decelerate when no input
            if self.velocity.length() > 0:
                self.velocity.x -= self.velocity.x * self.deceleration * dt
                self.velocity.y -= self.velocity.y * self.deceleration * dt

        # Cap velocity to max speed
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # Update position based on velocity
        self.rect.centerx += self.velocity.x * dt
        self.hitbox.centerx += self.velocity.x * dt
        self.rect.centery += self.velocity.y * dt
        self.hitbox.centery += self.velocity.y * dt

    def bullet_check(self):
        for bullet in self.bullet_g:
            if self.rect.colliderect(bullet.rect):
                self.health -= 1
                bullet.kill()
                if self.health:
                    play_sound('enemy_hit')
                    create_particles(self.rect.center,
                                     generate_particles(
                                         f'{self.name}_particle'),
                                     30, 15,
                                     self.particles_g)
                else:
                    self.player.score += self.score_weight
                    play_sound('explosion')
                    create_particles(self.rect.center,
                                     generate_particles('death_particle'),
                                     50, 30,
                                     self.particles_g)
                    item_type = random.choices(['health', 'ammo', ''],
                                               weights=(1, 1, 17), k=1)[0]
                    if item_type:
                        if item_type == 'health':
                            item = HealthBox(self.player, self.rect.center,
                                             2, self.particles_g, self.items_g)
                        if item_type == 'ammo':
                            item = AmmoBox(self.player, self.rect.center,
                                           10, self.particles_g, self.items_g)
                        self.items_g.add(item)
                    self.kill()

    def player_check(self):
        if self.damage_timer >= 120:
            if self.hitbox.colliderect(self.player.hitbox):
                self.player.health -= self.damage
                self.damage_timer = 0
                self.recovering = True  # Start recovering after hitting the player
                play_sound('hit')
                create_particles(self.player.rect.center,
                                 generate_particles('hit_particle'),
                                 50, 20,
                                 self.particles_g)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, pygame.Color('#306230'),
                         pygame.Rect(self.rect.centerx - 15, self.rect.y - 10,
                                     30, 5))
        pygame.draw.rect(screen, pygame.Color('#8bac0f'),
                         pygame.Rect(self.rect.centerx - 15, self.rect.y - 10,
                                     30 / self.max_health * self.health, 5))


class Square(Triangle):
    def __init__(self, pos, particles_g, bullet_g, items_g, player, *group):
        super().__init__(pos, particles_g, bullet_g, items_g, player, *group)
        self.image = load_image('square')
        self.name = 'square'
        self.rect = self.image.get_rect()

        self.rect.center = pos

        self.elapsed_time = 0

        if self.quotient > 1:
            self.quotient = 1

        self.max_speed = int(random.choices(range(2, 7),
                                            weights=(3, 3, 2, 2, 1), k=1)[0] *
                             self.quotient)

        if self.max_speed < 2:
            self.max_speed = 2

        self.health = 4
        self.max_health = 4
        self.damage = 2

        self.score_weight = 10

        self.hitbox = pygame.Rect(0, 0, 40, 40)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)

        self.acceleration = 0.1
        self.deceleration = 0.05
        self.velocity = pygame.Vector2(0, 0)


class Pentagon(Triangle):
    def __init__(self, pos, particles_g, bullet_g, items_g, enemy_bullet_g,
                 player, *group):
        super().__init__(pos, particles_g, bullet_g, items_g, player, *group)
        self.image = load_image('pentagon')
        self.name = 'pentagon'
        self.rect = self.image.get_rect()

        self.rect.center = pos

        self.elapsed_time = 0
        self.max_speed = 1
        self.health = 100
        self.max_health = 100
        self.damage = 5
        self.score_weight = 100

        self.dx = 0
        self.dy = 0

        self.particles_g = particles_g
        self.bullet_g = bullet_g
        self.player = player
        self.enemy_bullet_g = enemy_bullet_g

        self.damage_timer = 0

        self.hitbox = pygame.Rect(0, 0, 60, 60)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)

        self.acceleration = 0.025  # How quickly the player accelerates
        self.deceleration = 0.0125  # How quickly the player decelerates
        self.velocity = pygame.Vector2(0, 0)  # Current velocity

        self.cooldown = 0
        # self.c_time = 60 - (self.player.score - 200) // 50
        self.c_time = 60
        if self.c_time < 30:
            self.c_time = 30
        if self.c_time > 60:
            self.c_time = 60

    def update(self, screen, screen_rect, target_pos, dt):
        self.move(target_pos, dt)
        self.bullet_check()
        self.draw_health_bar(screen)
        self.player_check()

        # Handle damage cooldown and recovery
        if self.damage_timer < 120:
            self.damage_timer += dt
            self.recovering = True
        else:
            self.recovering = False  # Stop recovering when cooldown is done

        if self.cooldown < self.c_time:
            self.cooldown += dt

        self.shoot()

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, pygame.Color('#306230'),
                         pygame.Rect(self.rect.centerx - 30, self.rect.y - 10,
                                     60, 5))
        pygame.draw.rect(screen, pygame.Color('#8bac0f'),
                         pygame.Rect(self.rect.centerx - 30, self.rect.y - 10,
                                     60 / self.max_health * self.health, 5))

    def bullet_check(self):
        for bullet in self.bullet_g:
            if self.hitbox.colliderect(bullet.rect):
                self.health -= 1
                bullet.kill()
                if self.health:
                    play_sound('enemy_hit')
                    create_particles(self.rect.center,
                                     generate_particles(
                                         f'{self.name}_particle'),
                                     40, 30,
                                     self.particles_g)
                else:
                    self.player.score += self.score_weight
                    play_sound('explosion')
                    create_particles(self.rect.center,
                                     generate_particles('death_particle'),
                                     80, 60,
                                     self.particles_g)
                    for i in range(random.randint(4, 6)):
                        item_type = random.choice(['health', 'ammo'])
                        if item_type:
                            pos = (self.rect.centerx + random.randint(0, 100),
                                   self.rect.centery + random.randint(0, 100))
                            if item_type == 'health':
                                item = HealthBox(self.player, pos,
                                                 2, self.particles_g,
                                                 self.items_g)
                            if item_type == 'ammo':
                                item = AmmoBox(self.player, pos,
                                               10, self.particles_g,
                                               self.items_g)
                            self.items_g.add(item)
                    self.kill()

    def shoot(self):
        if self.cooldown >= self.c_time:
            play_sound('enemy_bullet', 0.2)
            create_enemy_bullet(self.rect.center, self.player.rect.center,
                                self.particles_g, self.enemy_bullet_g)
            self.cooldown = 0


class EnemySpawn:
    def __init__(self, group, particles_g, bullet_g, items_g, enemy_bullet_g,
                 player):
        self.elapsed_time = 0
        self.spawn_time = 5
        self.group = group
        self.particles_g = particles_g
        self.bullet_g = bullet_g
        self.player = player
        self.items_g = items_g
        self.enemy_bullet_g = enemy_bullet_g
        self.pentagon_count = 0
        self.score = 0
        self.max_enemy_count = 5

    def update(self, dt):
        self.elapsed_time += dt

        self.score = self.player.score
        self.max_enemy_count = (5 + self.player.score // 20 -
                                4 * self.player.score // 100 -
                                1 * self.player.score // 200 -
                                2 * self.player.score // 1000 -
                                5 * self.player.score // 2000)
        if self.max_enemy_count > 20:
            self.max_enemy_count = 20

        # self.spawn_time = 5 * (self.player.score // 20 -
        #                        4 * self.player.score // 100 -
        #                        1 * self.player.score // 200 -
        #                        2 * self.player.score // 1000 -
        #                        6 * self.player.score // 2000)

        if self.spawn_time > 30:
            self.spawn_time = 30

        if self.elapsed_time >= self.spawn_time and len(
                self.group) < self.max_enemy_count:
            self.elapsed_time = 0

            x = chain(range(-SW - 400, -SW - 200),
                      range(SW + 200, SW + 400))
            y = chain(range(-SH - 400, -SH - 200),
                      range(SH + 200, SH + 400))
            pos = random.choice(list(x)), random.choice(list(y))

            enemy_type = \
                random.choices(['square', 'triangle', 'pentagon'],
                               weights=(3, 7, 1), k=1)[0]

            self.generate_enemy(pos, enemy_type)

    def generate_enemy(self, pos, enemy_type):
        if enemy_type == 'square':
            enemy = Square(pos, self.particles_g, self.bullet_g,
                           self.items_g,
                           self.player, self.group)
            self.group.add(enemy)
        elif enemy_type == 'triangle':
            enemy = Triangle(pos, self.particles_g, self.bullet_g,
                             self.items_g,
                             self.player, self.group)
            self.group.add(enemy)
        else:
            if self.score > 200:
                if not any([e.name == 'pentagon' for e in self.group]):
                    enemy = Pentagon(pos, self.particles_g, self.bullet_g,
                                     self.items_g, self.enemy_bullet_g,
                                     self.player, self.group)

                    self.group.add(enemy)
