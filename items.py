import random

import pygame

from particles import create_particles, generate_particles
from sprites import Sprite
from load_image import load_image

from settings import play_sound


class Item(Sprite):
    def __init__(self, player, pos, image, particles_g, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.orig_pos = pos
        self.hitbox = pygame.Rect(0, 0, 60, 60)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)
        self.player = player
        self.particles_g = particles_g
        self.offset = 20
        self.direction = 1

    def update(self, dt):
        if self.rect.y > self.orig_pos[1] + self.offset:
            self.direction = -1
        if self.rect.y < self.orig_pos[1] - self.offset:
            self.direction = 1
        self.rect.y += dt * self.direction
        self.hitbox.y += dt * self.direction

        if self.hitbox.colliderect(self.player.rect):
            self.on_collide()

    def on_collide(self):
        pass


class HealthBox(Item):
    def __init__(self, player, pos, heal, particles_g, *group):
        super().__init__(player, pos, 'health', particles_g, *group)
        self.heal = heal

    def on_collide(self):
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


class AmmoBox(Item):
    def __init__(self, player, pos, ammo, particles_g, *group):
        self.type = random.choices((0, 1, 2), weights=(10, 5, 1), k=1)[0]
        images = ['ammo', 'shotgun_ammo', 'riffle_ammo']
        super().__init__(player, pos, images[self.type], particles_g, *group)
        self.ammo = [20, 10, 1]

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            create_particles(self.rect.center,
                             generate_particles('ammo_particle'),
                             20, 30,
                             self.particles_g)
            play_sound('ammo')

            ma = self.player.weapons[self.type]['max_ammo']
            a = self.player.weapons[self.type]['ammo']
            if ma >= a + self.ammo[self.type]:
                self.player.weapons[self.type]['ammo'] += self.ammo[self.type]
            else:
                self.player.weapons[self.type]['ammo'] = (
                    self.player.weapons[self.type]['max_ammo'])

            self.kill()


class SpeedBoost(Item):
    def __init__(self, player, pos, particles_g, *group):
        super().__init__(player, pos, 'speed_boost', particles_g, *group)

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.speed_boost = 2
            self.player.speed_boost_timer = self.player.max_speed_boost_time
            create_particles(self.rect.center,
                             generate_particles('speed_particle'),
                             20, 30,
                             self.particles_g)
            play_sound('speed_boost')
            self.kill()


class Shield(Item):
    def __init__(self, player, pos, particles_g, *group):
        super().__init__(player, pos, 'shield', particles_g, *group)

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.shield = True
            self.player.shield_timer = self.player.max_shield_time
            create_particles(self.rect.center,
                             generate_particles('shield_particle'),
                             20, 30,
                             self.particles_g)
            play_sound('shield')
            self.kill()


class Coin(Item):
    def __init__(self, player, pos, particles_g, *group):
        super().__init__(player, pos, 'coin', particles_g, *group)

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.coins += 1
            create_particles(self.rect.center,
                             generate_particles('coin_particle'),
                             20, 30,
                             self.particles_g)
            play_sound('coin', 0.2)
            self.kill()
