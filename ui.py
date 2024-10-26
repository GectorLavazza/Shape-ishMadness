import pygame

from sprites import Sprite
from settings import *


class Button(Sprite):
    def __init__(self, image, highlight, pos=(0, 0), *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.orig = image
        self.highlight = highlight
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.x <= mouse_pos[
            0] <= self.rect.x + self.orig.get_width() and self.rect.y <= \
                mouse_pos[1] <= self.rect.y + self.orig.get_height():
            self.image = self.highlight
        else:
            self.image = self.orig

        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                self.rect.collidepoint(args[0].pos)):
            return True

        return False


import pygame
from load_image import load_image


class Ui:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]


class Text(Ui):
    def __init__(self, screen, screen_size, font_size, color='white',
                 pos=(0, 0)):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size)
        self.pos = pos
        self.color = pygame.Color(color)

        self.render = self.font.render('', True, self.color)

    def update(self, message):
        self.render = self.font.render(str(message), True, self.color)
        pos = (self.pos[0] - self.render.get_width() // 2,
               self.pos[1] - self.render.get_height() // 2)
        self.screen.blit(self.render, pos)


class CoinsCount(Text):
    def __init__(self, screen, screen_size, font_size, color, pos=(0, 0)):
        self.coins_count = 0
        super().__init__(screen, screen_size, font_size, color, pos)

    def update(self, message):
        self.render = self.font.render(str(message), True, self.color)
        coin_image = load_image('coin')
        pos = (self.pos[0] - self.render.get_width(), self.pos[1])

        self.screen.blit(coin_image, (self.pos[0] + 10, self.pos[1] - 2))
        self.screen.blit(self.render, pos)


class ValueBar(Text):
    def __init__(self, screen, screen_size, max, image, pos):
        super().__init__(screen, screen_size, font_size=20,
                         color='white', pos=pos)
        self.max = max
        self.pos = pos[0] + 5, pos[1]
        self.image = load_image(image)

    def update(self, message):
        msg = message
        if message <= 0:
            msg = 0
        pygame.draw.rect(self.screen, pygame.Color('#306230'),
                         pygame.Rect(*self.pos, 200, 20))
        pygame.draw.rect(self.screen, pygame.Color('#8bac0f'),
                         pygame.Rect(*self.pos, 200 / self.max * msg, 20))
        self.render = self.font.render(f'{msg}/{self.max}', True, self.color)

        self.screen.blit(self.render, (110 - self.render.get_width() // 2, self.pos[1]))
        self.screen.blit(self.image, (6, self.pos[1] - 6))
