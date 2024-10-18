import pygame

from particles import create_particles, generate_particles
from sprites import Sprite
from load_image import load_image


class Player(Sprite):
    def __init__(self, bullets_g, particles_g, *group):
        super().__init__(*group)
        self.image = load_image('player')
        self.rect = self.image.get_rect()
        self.rect.center = (400, 400)
        self.score = 0
        self.speed = 5
        self.health = 10
        self.dx = 0
        self.dy = 0
        self.bullets_g = bullets_g
        self.paticles_g = particles_g

    def update(self, screen_rect, dt):
        direction = pygame.Vector2(self.dx, self.dy)
        if direction.length() > 0:
            direction = direction.normalize()
        self.rect.centerx += direction.x * self.speed * dt
        self.rect.centery += direction.y * self.speed * dt

    def shoot(self, mouse_pos):
        create_bullet(self.rect.center, mouse_pos,
                      self.paticles_g, self.bullets_g)


class Bullet(Sprite):
    def __init__(self, pos, target_pos, particles_g, *group):
        super().__init__(*group)
        self.image = load_image('bullet')
        self.rect = self.image.get_rect()

        self.rect.center = pos

        self.elapsed_time = 0
        self.existence_time = 60
        self.speed = 10

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
                             generate_particles('particle'),
                             10, 10,
                             self.particles_g)
            self.kill()


def create_bullet(position, target_pos, particles_g, group):
    Bullet(position, target_pos, particles_g, group)
