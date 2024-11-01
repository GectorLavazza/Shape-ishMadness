import pygame

from load_image import load_image
from particles import create_particles, generate_particles
from settings import RATIO
from settings import SW, SH
from sprites import Sprite


class Bullet(Sprite):
    def __init__(self, pos, target_pos, particles_g, e_time, damage, sound_player, *group):
        super().__init__(*group)
        self.image = load_image('bullet')
        self.rect = self.image.get_rect()

        self.rect.center = pos
        self.damage = damage

        self.elapsed_time = 0
        self.speed = 10
        self.existence_time = e_time

        self.particles_g = particles_g

        self.direction = pygame.Vector2(target_pos) - pygame.Vector2(pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        self.sound_player = sound_player

    def update(self, screen_rect, dt):
        self.rect.centerx += self.direction.x * self.speed * dt * RATIO
        self.rect.centery += self.direction.y * self.speed * dt * RATIO

        self.elapsed_time += dt
        self.check_e_time()

        if not (-5 <= self.rect.centerx <= SW + 5 and
                -5 <= self.rect.centery <= SH + 5):
            self.kill()

    def check_e_time(self):
        if self.elapsed_time >= self.existence_time:
            create_particles(self.rect.center,
                             generate_particles('bullet_particle3'),
                             10, 10,
                             self.particles_g)
            self.sound_player.play('bullet_explosion', 0.05)
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, pos, target_pos, particles_g, sound_player, *group):
        super().__init__(pos, target_pos, particles_g, 150, 1, sound_player, *group)
        self.image = load_image('enemy_bullet')
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def check_e_time(self):
        if self.elapsed_time >= self.existence_time:
            create_particles(self.rect.center,
                             generate_particles('enemy_bullet_particle'),
                             10, 10,
                             self.particles_g)
            self.sound_player.play('enemy_bullet_explosion', 0.2)
            self.kill()


def create_bullet(position, target_pos, damage, e_time, particles_g, sound_player, group):
    Bullet(position, target_pos, particles_g, e_time, damage, sound_player, group)


def create_enemy_bullet(position, target_pos, particles_g, sound_player, group):
    EnemyBullet(position, target_pos, particles_g, sound_player, group)
