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
        pos = (self.pos[0] - self.render.get_width() // 2, self.pos[1])
        self.screen.blit(self.render, pos)


class Timer(Ui):
    def __init__(self, seconds, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     200)
        self.seconds = seconds
        self.tick = 0

    def render(self):
        output = self.font.render(str(self.seconds), True, 'white')

        self.screen.blit(output, (self.width // 2 - output.get_width() // 2,
                                  self.height // 2 - output.get_height() // 2))

    def update(self):
        if self.seconds > 0:
            if self.tick > 0:
                self.tick -= 1
            if self.tick == 0:
                self.tick = 60
                self.seconds -= 1
            # if self.tick == 60 and self.seconds == 0:
            #     sfx = pygame.mixer.Sound('assets/sfx/Horn.mp3')
            #     sfx.set_volume(0.5)
            #     sfx.play()


class Startlabel(Timer):
    def __init__(self, seconds, screen, screen_size):
        super().__init__(seconds, screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     60)

    def render(self):
        output = self.font.render('Get Up!', True, 'black')

        for i in range(5 - self.seconds):
            self.screen.blit(output, (
                self.width // 2 - output.get_width() // 2,
                self.height // 2 - output.get_height() // 2 + 70 * i - 100))


class CoinsCount(Text):
    def __init__(self, screen, screen_size, font_size, color, dest=(0, 0)):
        self.coins_count = 0
        super().__init__(screen, screen_size, font_size, str(self.coins_count),
                         color, dest)

    def update(self):
        self.render = self.font.render(str(self.coins_count), True, self.color)
        self.dest = (self.width - self.render.get_width() - 60, 20)
        coin_image = load_image('coin_small')
        self.screen.blit(self.render, self.dest)
        self.screen.blit(coin_image, (430, 10))


class ValueBar(Text):
    def __init__(self, screen, screen_size, max, image, pos):
        super().__init__(screen, screen_size, font_size=20,
                         color='white', pos=pos)
        self.max = max
        self.pos = pos[0] + 5, pos[1]
        self.image = load_image(image)

    def update(self, message):
        pygame.draw.rect(self.screen, pygame.Color('#306230'),
                         pygame.Rect(*self.pos, 200, 20))
        pygame.draw.rect(self.screen, pygame.Color('#8bac0f'),
                         pygame.Rect(*self.pos, 20 * message, 20))
        self.render = self.font.render(f'{message}/{self.max}', True, self.color)

        self.screen.blit(self.render, (110 - self.render.get_width() // 2, self.pos[1]))
        self.screen.blit(self.image, (6, self.pos[1] - 6))
