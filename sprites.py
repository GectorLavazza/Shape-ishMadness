import random

import pygame

from load_image import load_image


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
