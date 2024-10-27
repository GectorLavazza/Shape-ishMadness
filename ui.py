import pygame

from sprites import Sprite
from settings import *

import pygame
from load_image import load_image


class Button(Sprite):
    def __init__(self, image, pos=(0, 0), *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.orig = image
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.orig_pos = pos

    def update(self, *args):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.x <= mouse_pos[
            0] <= self.rect.x + self.orig.get_width() and self.rect.y <= \
                mouse_pos[1] <= self.rect.y + self.orig.get_height():
            self.image = pygame.transform.smoothscale_by(self.orig, (1.05, 1.05))
        else:
            self.image = self.orig

        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
            args[0].key == 1 and self.rect.collidepoint(args[0].pos)):
            return True

        return False


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
                                     int(font_size * RATIO))
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

    def update(self, message, show_value=True):
        msg = message
        if message <= 0:
            msg = 0
        pygame.draw.rect(self.screen, pygame.Color('#306230'),
                         pygame.Rect(*self.pos, 200 * RATIO, 20 * RATIO))
        pygame.draw.rect(self.screen, pygame.Color('#8bac0f'),
                         pygame.Rect(*self.pos, 200 / self.max * msg * RATIO, 20 * RATIO))
        if show_value:
            self.render = self.font.render(f'{msg}/{self.max}', True, self.color)

            self.screen.blit(self.render, (110 * RATIO - self.render.get_width() // 2 * RATIO, self.pos[1]))

        self.screen.blit(self.image, (6, self.pos[1] - 6))


class Menu(Ui):
    def __init__(self, screen, screen_size, buttons_g, pos=(0, 0)):
        super().__init__(screen, screen_size)
        self.buttons_g = buttons_g
        self.menu = load_image('menu')
        self.bg = load_image('bg')
        self.pos = (pos[0] - self.menu.get_width() // 2,
                    pos[1] - self.menu.get_height() // 2)

    def update(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.menu, self.pos)

        for button in self.buttons_g:
            button.orig_pos = (500, 500)
            button.update()
