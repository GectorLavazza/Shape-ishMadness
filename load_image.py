import os

import pygame

from settings import RATIO


def load_image(name, color_key=None, scale=(RATIO, RATIO)):
    fullname = os.path.join("assets/sprites/", name + '.png')

    try:
        image = pygame.image.load(fullname).convert_alpha()
        # image = pygame.transform.smoothscale_by(image, scale)
    except pygame.error as e:
        print(f"Err: {e}")
        raise SystemExit(e)

    return image
