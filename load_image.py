import os

import pygame


def load_image(name):
    fullname = os.path.join("assets/sprites/", name + '.png')

    image = pygame.image.load(fullname).convert_alpha()

    return image
