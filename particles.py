import random

import pygame

from load_image import load_image
from settings import RATIO, SW, SH
from sprites import Sprite


class Particle(Sprite):
    def __init__(self, pos, dx, dy, particles, existence_time, *group):
        super().__init__(*group)
        self.particles = particles
        self.image = random.choice(self.particles)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.center = pos

        self.elapsed_time = 0
        self.existence_time = existence_time

    def update(self, screen_rect, dt):
        self.rect.x += self.velocity[0] * dt * RATIO
        self.rect.y += self.velocity[1] * dt * RATIO

        self.elapsed_time += dt

        if self.elapsed_time >= self.existence_time:
            self.kill()

        if not (-20 <= self.rect.centerx <= SW + 20 and
                -20 <= self.rect.centery <= SH + 20):
            self.kill()


def create_particles(position, particles, particle_count, existence_time,
                     *group):
    for _ in range(particle_count):
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        e_time = random.randint(1, existence_time)
        Particle(position, dx, dy, particles, e_time, *group)


def generate_particles(filename):
    particles = [load_image(filename)]
    for scale in [5, 10, 15]:
        particles.append(pygame.transform.scale(particles[0],
                                                (scale * RATIO, scale * RATIO)))
    return particles


def generate_text_particles(msg):
    font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                            20)
    particles = [font.render(msg, True, 'white')]
    for scale in [5, 10, 15]:
        particles.append(pygame.transform.scale(particles[0], (scale, scale)))
    return particles
