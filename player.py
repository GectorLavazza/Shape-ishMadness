import pygame
from pygame import Vector2

from particles import create_particles, generate_particles
from sprites import Sprite
from load_image import load_image

from settings import *


class Player(Sprite):
    def __init__(self, bullets_g, particles_g, enemy_bullet_g, *group):
        super().__init__(*group)
        self.image = load_image('player')
        self.rect = self.image.get_rect()
        self.rect.center = SW // 2, SH // 2
        self.hitbox = pygame.Rect(0, 0, 46, 46)
        self.hitbox.topleft = (
            self.rect.centerx + -self.hitbox.w // 2,
            self.rect.centery + -self.hitbox.h // 2)
        self.score = 0
        self.speed = 5  # Base speed
        self.max_speed = 8  # Maximum speed with sprint
        self.acceleration = 0.5  # How quickly the player accelerates
        self.deceleration = 0.1  # How quickly the player decelerates
        self.velocity = pygame.Vector2(0, 0)  # Current velocity
        self.health = 10
        self.max_health = 10
        self.dx = 0
        self.dy = 0
        self.bullets_g = bullets_g
        self.particles_g = particles_g
        self.enemy_bullet_g = enemy_bullet_g
        self.hold = False
        self.cooldown = 0
        self.c_time = 9
        self.hold_mode = False
        self.sprint = False
        self.damage = 1
        self.mode = 0

    def update(self, screen_rect, dt):
        input_direction = pygame.Vector2(self.dx, self.dy)

        if input_direction.length() > 0:
            input_direction = input_direction.normalize()

            # Accelerate towards input direction
            self.velocity.x += input_direction.x * self.acceleration * dt
            self.velocity.y += input_direction.y * self.acceleration * dt
        else:
            # Decelerate when no input
            if self.velocity.length() > 0:
                self.velocity.x -= self.velocity.x * self.deceleration * dt
                self.velocity.y -= self.velocity.y * self.deceleration * dt

        # Cap velocity to max speed
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # Update player position based on velocity
        if 0 <= self.rect.x + self.velocity.x * dt <= SW - self.rect.w:
            self.rect.centerx += self.velocity.x * dt
            self.hitbox.centerx += self.velocity.x * dt
        if 0 <= self.rect.y + self.velocity.y * dt <= SH - self.rect.h:
            self.rect.centery += self.velocity.y * dt
            self.hitbox.centery += self.velocity.y * dt

        # Handle shooting cooldown
        if self.cooldown < self.c_time:
            self.cooldown += dt

        # Sprint toggle
        if not self.hold:
            if self.sprint:
                self.max_speed = 8
            else:
                self.max_speed = 5
        else:
            self.max_speed = 4

        for bullet in self.enemy_bullet_g:
            if self.hitbox.colliderect(bullet.rect):
                self.health -= 1
                create_particles(self.rect.center,
                                 generate_particles('hit_particle'),
                                 50, 20,
                                 self.particles_g)
                play_sound('hit')
                bullet.kill()

    def shoot(self, mouse_pos):
        if self.cooldown >= self.c_time:
            play_sound('shoot2', 0.2)
            if self.mode == 0:
                create_bullet(self.rect.center, mouse_pos,
                              self.particles_g, self.bullets_g)
            elif self.mode == 1:
                for i in range(-30, 31, 10):
                    x = mouse_pos[0] - i
                    y = mouse_pos[1] - i
                    create_bullet(self.rect.center, (x, y),
                                  self.particles_g, self.bullets_g)
            elif self.mode == 2:
                for i in range(-30, 31, 10):
                    x = mouse_pos[0] - i
                    y = mouse_pos[1] - i
                    create_bullet(self.rect.center, (x, y),
                                  self.particles_g, self.bullets_g)
            self.cooldown = 0


class Bullet(Sprite):
    def __init__(self, pos, target_pos, particles_g, *group):
        super().__init__(*group)
        self.image = load_image('bullet')
        self.rect = self.image.get_rect()

        self.rect.center = pos

        self.elapsed_time = 0
        self.speed = 10
        self.existence_time = 60

        self.particles_g = particles_g

        self.direction = pygame.Vector2(target_pos) - pygame.Vector2(pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def update(self, screen_rect, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        self.elapsed_time += dt

        if self.elapsed_time >= self.existence_time:
            create_particles(self.rect.center,
                             generate_particles('bullet_particle3'),
                             10, 10,
                             self.particles_g)
            play_sound('bullet_explosion', 0.05)
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, pos, target_pos, particles_g, *group):
        super().__init__(pos, target_pos, particles_g, *group)
        self.image = load_image('enemy_bullet')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.existence_time = 150

    def update(self, screen_rect, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        self.elapsed_time += dt

        if self.elapsed_time >= self.existence_time:
            create_particles(self.rect.center,
                             generate_particles('enemy_bullet_particle'),
                             10, 10,
                             self.particles_g)
            play_sound('enemy_bullet_explosion', 0.2)
            self.kill()


def create_bullet(position, target_pos, particles_g, group):
    Bullet(position, target_pos, particles_g, group)


def create_enemy_bullet(position, target_pos, particles_g, group):
    EnemyBullet(position, target_pos, particles_g, group)
