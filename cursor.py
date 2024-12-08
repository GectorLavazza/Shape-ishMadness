import pygame

from load_image import load_image
from sprites import Sprite


class Cursor(Sprite):
    def __init__(self, player, *group):
        super().__init__(*group)
        self.image = load_image('cursor')
        self.rect = self.image.get_rect()
        self.player = player

    def update(self, render=True):
        mouse_pos = pygame.mouse.get_pos()
        mouseFocus = pygame.mouse.get_focused()

        # if self.player.health < 5:
        #     self.image = load_image('cursor_attention')
        # else:
        self.image = load_image('cursor')

        if mouseFocus:
            self.rect.topleft = mouse_pos
        else:
            self.rect.topleft = (-100, -100)
