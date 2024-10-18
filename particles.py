import pygame
from sprites import Sprite
import random
from load_image import load_image



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

    def update(self, screen_rect, dt, fps):

        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt

        self.elapsed_time += dt

        if self.elapsed_time >= self.existence_time:
            self.kill()


def create_particles(position, particles, particle_count, existence_time, *group):
    for _ in range(particle_count):
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        e_time = random.randint(1, existence_time)
        Particle(position, dx, dy, particles, e_time, *group)


def generate_particles(filename):
    particles = [load_image(filename)]
    for scale in [1, 2, 5]:
        particles.append(pygame.transform.scale(particles[0], (scale, scale)))
    return particles
