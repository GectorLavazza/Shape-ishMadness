import pygame.draw

from load_image import load_image
from settings import *
from sprites import Sprite


class Button(Sprite):
    def __init__(self, screen, screen_size, image, highlighted, pos=(0, 0),
                 *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.orig = load_image(image)
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.orig_pos = pos
        self.highlighted = load_image(highlighted)
        self.screen = screen
        self.hidden_msg_font = pygame.font.Font(
            'assets/fonts/PixelOperator8-Bold.ttf',
            15)

    def update(self, *args):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.x <= mouse_pos[
            0] <= self.rect.x + self.orig.get_width() and self.rect.y <= \
                mouse_pos[1] <= self.rect.y + self.orig.get_height():
            self.image = self.highlighted
        else:
            self.image = self.orig

        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                self.rect.collidepoint(args[0].pos)):
            return True

        return False

    def draw_hint(self):
        hint = 'sigmo'
        hint_render = self.hidden_msg_font.render(hint,
                                                  True,
                                                  'white')
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         pygame.Rect(
                             pygame.mouse.get_pos()[0] + 14 - 70,
                             pygame.mouse.get_pos()[1] + 14,
                             hint_render.get_width() + 8,
                             hint_render.get_height() + 8))
        self.screen.blit(hint_render, (
            pygame.mouse.get_pos()[0] + 14 + 4 - 70,
            pygame.mouse.get_pos()[1] + 14 + 4))


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
                         pygame.Rect(*self.pos, 200 / self.max * msg * RATIO,
                                     20 * RATIO))
        if show_value:
            self.render = self.font.render(f'{msg}/{self.max}', True,
                                           self.color)

            self.screen.blit(self.render, (
                110 * RATIO - self.render.get_width() // 2 * RATIO,
                self.pos[1]))

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


class UpgradesMenu(Text):
    def __init__(self, screen, screen_size, data, player):
        super().__init__(screen, screen_size, 20)
        self.image = load_image('menu')
        self.data = data
        self.pos = (self.width // 2 - self.image.get_width() // 2,
                    self.height // 2 - self.image.get_height() // 2)
        self.bg = pygame.Surface(
            (self.width, self.height))
        self.bg.set_alpha(128)
        self.bg.fill((0, 0, 0))

        self.current = [0, 0]
        self.current_heading = ''
        self.current_name = ''

        self.player = player

    def update(self, screen):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.image, self.pos)

        a = len(list(self.data.data.keys()))

        for i in range(a):

            heading = list(self.data.data.keys())[i]
            if i == self.current[0]:
                self.current_heading = heading
            x, y = (self.pos[0] * 1.25 + self.image.get_width() // a * i,
                    self.pos[1] + 40)
            render = Text(screen, (self.width, self.height), 20, pos=(x, y),
                          color='red')
            render.update(heading)

            for j in range(len(list(self.data.data[heading].keys()))):
                name = list(self.data.data[heading].keys())[j]
                if j == self.current[1] and i == self.current[0]:
                    self.current_name = name
                x, y = (self.pos[0] * 1.25 + self.image.get_width() // a * i,
                        self.pos[1] + 80 + (150 * j + 1))
                render = Text(screen, (self.width, self.height), 20,
                              pos=(x, y))
                render.update(name)

                v = self.data.data[heading][name][0]
                min_v = self.data.data[heading][name][1]
                max_v = self.data.data[heading][name][2]
                c = self.data.data[heading][name][3]
                ml = abs(max_v - min_v) // abs(c) + 1
                l = 1 + abs(v - min_v) // abs(c)
                p = self.data.data[heading][name][4] * l

                if [i, j] == self.current:
                    color = 'magenta'
                    pygame.draw.rect(self.screen, 'magenta', (x - 18, y + 72, 40, 5))
                    if l < ml:
                        price = Text(screen, (self.width, self.height), 20,
                                     pos=(x, y + 100), color='yellow')
                        price.update(p)
                else:
                    color = '#9bbc0f'

                value = Text(screen, (self.width, self.height), 20,
                             pos=(x, y + 50), color=color)

                value.update(f'{l}/{ml}')


    def buy(self):
        i, j = self.current

        heading = list(self.data.data.keys())[i]
        name = list(self.data.data[heading].keys())[j]

        v = self.data.data[heading][name][0]
        min_v = self.data.data[heading][name][1]
        max_v = self.data.data[heading][name][2]
        c = self.data.data[heading][name][3]
        ml = abs(max_v - min_v) // abs(c) + 1
        l = 1 + abs(v - min_v) // abs(c)
        p = self.data.data[heading][name][4] * l

        if c > 0:
            if v + c <= max_v and self.player.coins - p >= 0:
                self.data.data[heading][name][0] += c
                self.player.coins -= p
        elif c < 0:
            if v + c >= max_v and self.player.coins - p >= 0:
                self.data.data[heading][name][0] += c
                self.player.coins -= p


class Data:
    def __init__(self, data):
        self.data = data
