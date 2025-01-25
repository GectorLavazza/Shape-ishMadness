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
                 pos=(0, 0), center_align=True, right_align=False):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     int(font_size * RATIO))
        self.pos = pos
        self.color = pygame.Color(color)
        self.center_align = center_align
        self.right_align = right_align

        self.render = self.font.render('', True, self.color).convert_alpha()
        self.rect = self.render.get_rect()

    def update(self, message):
        self.render = self.font.render(str(message), True,
                                       self.color).convert_alpha()
        self.rect = self.render.get_rect()
        if self.center_align:
            pos = (self.pos[0] - self.render.get_width() // 2,
                   self.pos[1] - self.render.get_height() // 2)
        elif self.right_align:
            pos = (self.pos[0] - self.render.get_width(),
                   self.pos[1] - self.render.get_height() // 2)
        else:
            pos = (self.pos[0],
                   self.pos[1] - self.render.get_height() // 2)
        self.screen.blit(self.render, pos)


class ResourceCount(Text):
    def __init__(self, screen, screen_size, font_size, color, image,
                 pos=(0, 0)):
        self.coins_count = 0
        super().__init__(screen, screen_size, font_size, color, pos)
        self.image = load_image(image)

    def update(self, message):
        self.render = self.font.render(str(message), True, self.color)
        pos = (self.pos[0] - self.render.get_width(), self.pos[1])

        self.screen.blit(self.image, (self.pos[0] + 10, self.pos[1] - 2))
        self.screen.blit(self.render, pos)


class XpBar(Text):
    def __init__(self, screen, screen_size, font_size, color, image,
                 pos=(0, 0)):
        super().__init__(screen, screen_size, font_size, color, pos)
        self.image = load_image(image)

    def update(self, xp):
        l = xp // 30

        self.render = self.font.render(str(l), True, self.color)

        pos = (
        self.pos[0] - self.render.get_width() // 2 - 53, self.pos[1] - 5)
        xp_pos = (self.pos[0] - 103, self.pos[1] + 20)
        l_pos = (self.pos[0] - 103, self.pos[1])

        self.screen.blit(self.image, (self.pos[0] + 10, self.pos[1]))

        pygame.draw.rect(self.screen, pygame.Color('#306230'),
                         pygame.Rect(*l_pos, 100, 15))
        pygame.draw.rect(self.screen, pygame.Color('#8bac0f'),
                         pygame.Rect(*l_pos, 100 / 20 * l, 15))

        pygame.draw.rect(self.screen, pygame.Color('#306230'),
                         pygame.Rect(*xp_pos, 100, 10))
        pygame.draw.rect(self.screen, pygame.Color('#8bac0f'),
                         pygame.Rect(*xp_pos, 100 / 30 * (xp % 30), 10))

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
                120 * RATIO - self.render.get_width() // 2 * RATIO,
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
    def __init__(self, screen, screen_size, data, player, sound_player):
        super().__init__(screen, screen_size, 20)
        self.image = load_image('menu')

        self.w, self.h = SW * 3 // 4,  SH * 3 // 4
        self.pos = (SW // 2 - self.w // 2,
                    SH // 2 - self.h // 2)
        self.rect = pygame.Rect(self.w, self.h, *self.pos)

        self.data = data

        self.screen = screen

        self.bg = pygame.Surface(
            (SW, SH))
        self.bg.set_alpha(128)
        self.bg.fill('black')

        self.current = [0, 0]
        self.current_heading = ''
        self.current_name = ''

        self.player = player
        self.sound_player = sound_player
        self.headings, self.names, self.surface = self.oninit()

        self.do = True

        self.message = Text(screen, (self.width, self.height), 30,
                            pos=(self.pos[0] + self.w // 2,
                                 self.pos[1] + self.h - 40), color='red',
                            center_align=True)

    def update(self, screen):
        screen.blit(self.surface, self.pos)

        a = len(list(self.data.data.keys()))

        for i in range(a):

            heading = list(self.data.data.keys())[i]
            self.headings[i].update(heading)
            if i == self.current[0]:
                self.current_heading = heading

            for j in range(len(list(self.data.data[heading].keys()))):
                x, y = (self.pos[0] * 1.5 + self.w // a * i,
                        self.pos[1] + 80 + (150 * j + 1))

                name = list(self.data.data[heading].keys())[j]
                if j == self.current[1] and i == self.current[0]:
                    self.current_name = name
                self.names[i][j].update(name)

                v = self.data.data[heading][name][0]
                min_v = self.data.data[heading][name][1]
                max_v = self.data.data[heading][name][2]
                c = self.data.data[heading][name][3]
                ml = abs(max_v - min_v) // abs(c) + 1
                l = 1 + abs(v - min_v) // abs(c)
                p = self.data.data[heading][name][4] * l

                colliderect = pygame.Rect(x - 50, y + 30, 100, 60)
                # pygame.draw.rect(screen, '#9bbc0f', colliderect)

                color_back = '#306230'
                color_front = '#8bac0f'

                if l < ml:
                    if colliderect.collidepoint(pygame.mouse.get_pos()):
                        self.current = [i, j]
                        upd = True

                        if heading == 'Blaster+':
                            blaster = self.data.data['Blaster']
                            blaster_check = [blaster['Dmg'][0] >= 5,
                                             blaster['Cooldown'][0] <= 15,
                                             blaster['Max Ammo'][0] >= 200]

                            if not all(blaster_check):
                                self.message.update(
                                    'Dmg lvl 5, Cooldown lvl 4, Max Ammo lvl 4 needed')
                                upd = False

                        if upd:
                            color_back = '#cf9dcf'
                            color_front = '#7453f0'

                            price = Text(screen, (self.width, self.height), 20,
                                         pos=(x, y + 130), color='yellow')
                            price.update(p)

                            lvl = Text(screen, (self.width, self.height), 20,
                                       pos=(x, y + 100), color='white')
                            lvl.update(f'lvl {l}')

                pygame.draw.rect(screen, pygame.Color(color_back),
                                 pygame.Rect(x - 40, y + 50,
                                             80, 20))
                pygame.draw.rect(screen, pygame.Color(color_front),
                                 pygame.Rect(x - 40, y + 50,
                                             80 / ml * l, 20))

    def buy(self):
        i, j = self.current
        self.do = True

        heading = list(self.data.data.keys())[i]
        name = list(self.data.data[heading].keys())[j]

        v = self.data.data[heading][name][0]
        min_v = self.data.data[heading][name][1]
        max_v = self.data.data[heading][name][2]
        c = self.data.data[heading][name][3]
        ml = abs(max_v - min_v) // abs(c) + 1
        l = 1 + abs(v - min_v) // abs(c)
        p = self.data.data[heading][name][4] * l
        xp = self.data.data[heading][name][5]

        if heading == 'Blaster+':
            blaster = self.data.data['Blaster']
            blaster_check = [blaster['Dmg'][0] >= 5,
                             blaster['Cooldown'][0] <= 15,
                             blaster['Max Ammo'][0] >= 200]
            if not all(blaster_check):
                self.do = False

        if self.do:
            if c > 0:
                if v + c <= max_v and self.player.coins - p >= 0:
                    self.take_coins(heading, name, c, p, xp)
                else:
                    self.do = False
            elif c < 0:
                if v + c >= max_v and self.player.coins - p >= 0:
                    self.take_coins(heading, name, c, p, xp)
                else:
                    self.do = False

    def take_coins(self, heading, name, c, p, xp):
        self.sound_player.play('click')

        self.data.data[heading][name][0] += c
        self.player.coins -= p

        self.player.xp += xp

    def oninit(self):
        surface = pygame.Surface((self.w,
                                  self.h))
        surface = surface.convert_alpha()
        surface.fill('#0b2b0b')
        # surface.blit(self.image, (0, 0))
        # surface = surface.convert_alpha()
        headings = []
        names = []

        a = len(list(self.data.data.keys()))
        for i in range(a):
            heading = list(self.data.data.keys())[i]
            xh, yh = (self.pos[0] * 1.5 + self.w // a * i,
                      self.pos[1] + 40)
            hr = Text(self.screen, (self.width, self.height), 25, pos=(xh, yh),
                      color='#9bbc0f')
            headings.append(hr)
            names_row = []

            for j in range(len(list(self.data.data[heading].keys()))):
                yn = self.pos[1] + 100 + (150 * j + 1)
                nr = Text(self.screen, (self.width, self.height), 25,
                          pos=(xh, yn), color='#9bbc0f')
                names_row.append(nr)

            names.append(names_row)

        return headings, names, surface


class Data:
    def __init__(self, data):
        self.data = data
