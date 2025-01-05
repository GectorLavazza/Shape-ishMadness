import pygame

pygame.display.init()
screen_info = pygame.display.Info()

FPS = 30

# brightest to darkest
PALETTE = ['#9bbc0f', '#8bac0f', '#306230', '#0f380f']

# [current, min, max, step, price_step, xp]
DATA = d = {
    "Player": {"Hp": [10, 10, 30, 2, 50, 10],
               "Crit %": [1, 1, 5, 1, 50, 7],
               "Spd": [5, 5, 8, 1, 5, 5]},
    "Blaster": {"Dmg": [1, 1, 10, 1, 10, 7],
                "Cooldown": [30, 30, 5, -5, 5, 2],
                'Max Ammo': [50, 50, 500, 50, 10, 3]},
    'Blaster+': {'Range': [60, 60, 240, 30, 20, 2],
                 'Amount': [1, 1, 21, 2, 30, 5],
                 'Angle': [10, 10, 90, 10, 50, 6]},
    "Spd Boost": {"Time": [600, 600, 1200, 100, 40, 7],
                  "Boost": [1, 1, 4, 1, 60, 9]},
    "Shield": {"Time": [600, 600, 1200, 100, 40, 8],
               "Protection": [1, 1, 9, 1, 60, 10]},
    "Magnet": {"Time": [300, 300, 600, 100, 40, 5],
               "Force": [5, 5, 15, 2, 60, 7]}
}

RESTRICTIONS = {
    "Player": {"Hp": {22: 5000},
               "Crit %": {2: 2000},
               "Spd": {6: 2000}},
    "Blaster": {"Dmg": [1, 1, 10, 1, 10, 7],
                "Cooldown": [30, 30, 5, -5, 5, 2],
                'Max Ammo': [50, 50, 500, 50, 10, 3]},
    'Blaster+': {'Range': [60, 60, 240, 30, 20, 2],
                 'Amount': [1, 1, 21, 2, 30, 5],
                 'Angle': [10, 10, 90, 10, 50, 6]},
    "Spd Boost": {"Time": [600, 600, 1200, 100, 40, 7],
                  "Boost": [1, 1, 4, 1, 60, 9]},
    "Shield": {"Time": [600, 600, 1200, 100, 40, 8],
               "Protection": [1, 1, 9, 1, 60, 10]},
    "Magnet": {"Time": [300, 300, 600, 100, 40, 5],
               "Force": [5, 5, 15, 2, 60, 7]}

}

MAX_XP = 0
for d in DATA:
    e = DATA[d]
    for i in e:
        s = e[i]
        MAX_XP += (s[2] - s[1]) // s[3] * s[5]

CHEAT_DATA = {
    "Player": {"Hp": [30, 10, 30, 2, 50],
               "Crit %": [5, 1, 5, 1, 50],
               "Spd": [8, 5, 8, 1, 50]},
    "Blaster": {"Dmg": [10, 1, 10, 1, 20],
                "Cooldown": [5, 30, 5, -5, 5],
                'Max Ammo': [500, 50, 500, 50, 10]},
    'Blaster+': {'Range': [240, 60, 240, 30, 20],
                 'Amount': [21, 1, 21, 2, 30],
                 'Angle': [90, 10, 90, 10, 50]},
    "Spd Boost": {"Time": [1200, 600, 1200, 100, 40],
                  "Boost": [4, 1, 4, 1, 60]},
    "Shield": {"Time": [1200, 600, 1200, 100, 40],
               "Protection": [9, 1, 9, 1, 60]},
    "Magnet": {"Time": [600, 300, 600, 100, 40],
               "Force": [15, 5, 15, 2, 60]}
}

DATA_WITH_POWERS = {
    "Player": {"Hp": [10, 10, 30, 2, 50],
               "Crit %": [1, 1, 5, 1, 50],
               "Spd": [5, 5, 8, 1, 50]},
    "Blaster": {"Dmg": [1, 1, 10, 1, 20],
                "Cooldown": [30, 30, 5, -5, 5],
                'Max Ammo': [50, 50, 500, 50, 10]},
    'Blaster+': {'Range': [60, 60, 240, 30, 20],
                 'Amount': [1, 1, 21, 2, 30],
                 'Angle': [10, 10, 90, 10, 50]},
    "Spd Boost": {"Time": [600, 600, 1200, 100, 40],
                  "Boost": [1, 1, 4, 1, 60]},
    "Shield": {"Time": [600, 600, 1200, 100, 40],
               "Protection": [1, 1, 9, 1, 60]},
    "Magnet": {"Time": [300, 300, 600, 100, 40],
               "Force": [5, 5, 15, 2, 60]},
    "Powers": {"Thorns": [0, 0, 5, 1, 500],
               "Spd Theft": [0, 0, 5, 1, 500],
               "Rage": [0, 0, 8, 1, 500]}
}

ITEMS_WEIGHTS = (8, 10, 5, 3, 4, 70)


def fit_aspect_ratio(screen_width, screen_height,
                     target_width=1920, target_height=1080):
    # Calculate the aspect ratio
    aspect_ratio = target_width / target_height

    # Calculate the maximum width and height that fit within the screen dimensions
    max_width = screen_width
    max_height = screen_height

    # Calculate the height based on the max width
    height_based_on_width = max_width / aspect_ratio
    if height_based_on_width <= max_height:
        return int(max_width), int(height_based_on_width)

    # Calculate the width based on the max height
    width_based_on_height = max_height * aspect_ratio
    if width_based_on_height <= max_width:
        return int(width_based_on_height), int(max_height)

    # If neither fits, return the largest fitting size
    return int(max_width), int(max_height)


sw, sh = screen_info.current_w, screen_info.current_h
# sw, sh = 1920, 1080
SW, SH = 1280, 720
RATIO = 1

SONGS = ['shape-ish_madness', 'metal_shape_synth_ver', 'metal_shape']


def set_screen(size):
    pygame.display.set_caption('Shape-ish Madness')
    flags = pygame.DOUBLEBUF | pygame.SCALED
    screen = pygame.display.set_mode(size, flags, depth=8, vsync=1)
    screen_rect = (0, 0, size[0], size[1])

    return screen, size, screen_rect


def render_hitbox(screen, player, enemies, p_bullets, e_bullets, items,
                  rect=True, hitbox=True):
    if rect:
        pygame.draw.rect(screen, pygame.Color('blue'), player.rect)

    for enemy in enemies:
        if rect:
            pygame.draw.rect(screen, pygame.Color('purple'), enemy.rect)
        if hitbox:
            pygame.draw.rect(screen, pygame.Color('red'), enemy.hitbox)

    for bullet in p_bullets:
        if rect or hitbox:
            pygame.draw.rect(screen, pygame.Color('yellow'), bullet.rect)

    for bullet in e_bullets:
        if rect or hitbox:
            pygame.draw.rect(screen, pygame.Color('orange'), bullet.rect)

    for item in items:
        if hitbox:
            pygame.draw.rect(screen, pygame.Color('white'), item.hitbox)
        if rect:
            pygame.draw.rect(screen, pygame.Color('grey'), item.rect)

    if hitbox:
        pygame.draw.rect(screen, pygame.Color('green'), player.hitbox)
