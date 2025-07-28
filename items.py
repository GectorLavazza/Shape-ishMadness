import random

import pygame

from load_image import load_image
from particles import create_particles, generate_particles
from settings import RATIO, SW, SH
from sprites import Sprite


class Item(Sprite):
    def __init__(self, player, pos, image, particles_g, sound_player, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.orig_pos = pos
        self.hitbox = pygame.Rect(0, 0, self.rect.w * 2, self.rect.h * 2)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)
        self.player = player
        self.particles_g = particles_g
        self.offset = 20
        self.direction = 1
        self.velocity = 0
        self.timer = 1200
        self.group = group[0]
        self.sound_player = sound_player

    def update(self, dt):
        # self.handle_overlap(self.group)

        if self.rect.y > self.orig_pos[1] + self.offset:
            self.direction = -1
        if self.rect.y < self.orig_pos[1] - self.offset:
            self.direction = 1
        self.rect.y += dt * self.direction * RATIO
        self.hitbox.y += dt * self.direction * RATIO

        self.timer -= dt
        if self.timer <= 0:
            self.kill()

        if not (-20 <= self.rect.centerx <= SW + 20 and
                -20 <= self.rect.centery <= SH + 20):
            self.kill()

        if self.hitbox.colliderect(self.player.rect):
            self.on_collide()

    def on_collide(self):
        pass

    def handle_overlap(self, all_items):
        count = 0
        for other in all_items:
            if other != self and self.hitbox.colliderect(other.hitbox):
                count += 1
                if count > 20:
                    self.kill()


class HealthBox(Item):
    def __init__(self, player, pos, heal, particles_g, sound_player, *group):
        super().__init__(player, pos, 'health', particles_g, sound_player,
                         *group)
        self.heal = heal

    def on_collide(self):
        if not self.player.hardcore:
            if self.player.health + self.heal <= self.player.max_health:
                self.player.health += self.heal
            else:
                self.player.health = self.player.max_health

            create_particles(self.rect.center,
                             generate_particles('heal_particle'),
                             20, 30,
                             self.particles_g)
            self.sound_player.play('heal')
        self.kill()


class AmmoBox(Item):
    def __init__(self, player, pos, particles_g, sound_player, *group):
        image = 'ammo'
        super().__init__(player, pos, image, particles_g, sound_player, *group)
        self.ammo = 50

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            create_particles(self.rect.center,
                             generate_particles('ammo_particle'),
                             20, 30,
                             self.particles_g)
            self.sound_player.play('ammo')

            ma = self.player.blaster['Max Ammo'][0]
            a = self.player.ammo
            if ma >= a + self.ammo:
                self.player.ammo += self.ammo
            else:
                self.player.ammo = (
                    self.player.blaster['Max Ammo'][0])

            self.kill()


class SpeedBoost(Item):
    def __init__(self, player, pos, particles_g, sound_player, *group):
        super().__init__(player, pos, 'speed_boost', particles_g, sound_player,
                         *group)

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.speed_boost = self.player.data['Spd Boost']['Boost'][0]
            self.player.speed_boost_timer = self.player.max_speed_boost_time
            create_particles(self.rect.center,
                             generate_particles('speed_particle'),
                             20, 30,
                             self.particles_g)
            self.sound_player.play('speed_boost')
            self.kill()


class Shield(Item):
    def __init__(self, player, pos, particles_g, sound_player, *group):
        super().__init__(player, pos, 'shield', particles_g, sound_player,
                         *group)

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.shield = True
            self.player.shield_timer = self.player.max_shield_time
            create_particles(self.rect.center,
                             generate_particles('shield_particle'),
                             20, 30,
                             self.particles_g)
            self.sound_player.play('shield')
            self.kill()


class Magnet(Item):
    def __init__(self, player, pos, particles_g, sound_player, *group):
        super().__init__(player, pos, 'magnet', particles_g, sound_player,
                         *group)

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.magnet = True
            self.player.magnet_timer = self.player.max_magnet_time
            create_particles(self.rect.center,
                             generate_particles('magnet_particle'),
                             20, 30,
                             self.particles_g)
            self.sound_player.play('magnet')
            self.kill()


class Coin(Item):
    def __init__(self, player, pos, particles_g, sound_player, *group):

        super().__init__(player, pos, 'coin', particles_g, sound_player,
                         *group)

        self.weight = 1
        self.particles_amount = 20
        self.particles_e_time = 30

        if random.randint(1, 100) == 1:
            self.weight = 50
            self.particles_amount = 40
            self.particles_e_time = 60
            self.image = pygame.transform.scale_by(self.image,
                                                   (1.5, 1.5)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.orig_pos = pos
            self.hitbox = pygame.Rect(0, 0, self.rect.w * 2, self.rect.h * 2)
            self.hitbox.topleft = (
                self.rect.centerx + - self.hitbox.w // 2,
                self.rect.centery + - self.hitbox.h // 2)

        self.acceleration = 0.95
        self.deceleration = 0.95
        self.max_speed = self.player.data['Magnet']['Force'][0]

        self.velocity = pygame.Vector2(0, 0)
        self.just_ended = False

    def update(self, dt):
        self.max_speed = self.player.data['Magnet']['Force'][0]

        self.handle_overlap(self.group)

        if self.player.magnet:
            self.just_ended = False
            self.move_towards_player(dt)
        else:
            if not self.just_ended:
                self.just_ended = True
                self.orig_pos = self.rect.center
            if self.rect.y > self.orig_pos[1] + self.offset:
                self.direction = -1
            if self.rect.y < self.orig_pos[1] - self.offset:
                self.direction = 1
            self.rect.y += dt * self.direction * RATIO
            self.hitbox.y += dt * self.direction * RATIO

            self.timer -= dt
            if self.timer <= 0:
                self.kill()

        if not (-20 * RATIO <= self.rect.centerx <= SW + 20 * RATIO and
                -20 * RATIO <= self.rect.centery <= SH + 20 * RATIO):
            self.kill()

        if self.hitbox.colliderect(self.player.rect):
            self.on_collide()

    def on_collide(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.coins += self.weight
            create_particles(self.rect.center,
                             generate_particles('coin_particle'),
                             self.particles_amount, self.particles_e_time,
                             self.particles_g)
            self.sound_player.play('coin', 0.2)
            self.kill()

    def move_towards_player(self, dt):
        direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(
            self.rect.center)

        if direction.length() > 0:
            direction = direction.normalize()

        self.velocity.x += direction.x * self.acceleration * dt * RATIO
        self.velocity.y += direction.y * self.acceleration * dt * RATIO

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.rect.centerx += self.velocity.x * dt * RATIO
        self.hitbox.centerx += self.velocity.x * dt * RATIO
        self.rect.centery += self.velocity.y * dt * RATIO
        self.hitbox.centery += self.velocity.y * dt * RATIO
