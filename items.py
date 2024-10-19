import pygame

from particles import create_particles, generate_particles
from sprites import Sprite
from load_image import load_image

from settings import play_sound


class HealthBox(Sprite):
    def __init__(self, player, pos, heal, particles_g, *group):
        super().__init__(*group)
        self.image = load_image('health')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.orig_pos = pos
        self.player = player
        self.heal = heal
        self.particles_g = particles_g
        self.offset = 20
        self.direction = 1

    def update(self, dt):
        if self.rect.y > self.orig_pos[1] + self.offset:
            self.direction = -1
        if self.rect.y < self.orig_pos[1] - self.offset:
            self.direction = 1
        self.rect.y += 1 * dt * self.direction
        if self.rect.colliderect(self.player.hitbox):
            if self.player.health + self.heal <= self.player.max_health:
                self.player.health += self.heal
            else:
                self.player.health = self.player.max_health

            create_particles(self.rect.center,
                             generate_particles('heal_particle'),
                             20, 30,
                             self.particles_g)
            play_sound('heal')
            self.kill()


class AmmoBox(Sprite):
    def __init__(self, player, pos, ammo, particles_g, *group):
        super().__init__(*group)
        self.image = load_image('ammo')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.orig_pos = pos
        self.player = player
        self.ammo = ammo
        self.particles_g = particles_g
        self.offset = 20
        self.direction = 1

    def update(self, dt):
        if self.rect.y > self.orig_pos[1] + self.offset:
            self.direction = -1
        if self.rect.y < self.orig_pos[1] - self.offset:
            self.direction = 1
        self.rect.y += 1 * dt * self.direction
        if self.rect.colliderect(self.player.hitbox):
            create_particles(self.rect.center,
                             generate_particles('ammo_particle'),
                             20, 30,
                             self.particles_g)
            play_sound('ammo')
            self.kill()
