import pygame
import random
from itertools import *

from particles import create_particles, generate_particles
from sprites import Sprite
from load_image import load_image


class Enemy(Sprite):
    def __init__(self, pos, particles_g, bullet_g, image, speed, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()

        self.rect.center = pos

        self.elapsed_time = 0
        self.speed = speed

        self.dx = 0
        self.dy = 0

        self.particles_g = particles_g
        self.bullet_g = bullet_g

    def update(self, screen_rect, target_pos, dt):

        direction = pygame.Vector2(target_pos) - pygame.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        self.rect.centerx += direction.x * self.speed * dt
        self.rect.centery += direction.y * self.speed * dt

        self.bullet_check()

    def bullet_check(self):

        for bullet in self.bullet_g:
            if self.rect.colliderect(bullet.rect):
                create_particles(self.rect.center,
                                 generate_particles('particle'),
                                 50, 20,
                                 self.particles_g)
                bullet.kill()
                self.kill()



class EnemySpawn:
    def __init__(self, group, particles_g, bullet_g):
        self.elapsed_time = 0
        self.spawn_time = 60
        self.group = group
        self.particles_g = particles_g
        self.bullet_g = bullet_g

    def update(self, dt):
        self.elapsed_time += dt

        if self.elapsed_time >= self.spawn_time:
            self.elapsed_time = 0

            x = chain(range(-400, -200), range(1000, 1200))
            y = chain(range(-400, -200), range(1000, 1200))
            pos = random.choice(list(x)), random.choice(list(y))
            image = random.choice(['square', 'triangle'])
            speed = random.randint(10, 70) / 10
            enemy = Enemy(pos, self.particles_g, self.bullet_g,
                          image, speed, self.group)
            self.group.add(enemy)
