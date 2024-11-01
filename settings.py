import pygame

pygame.display.init()
screen_info = pygame.display.Info()

FPS = 60

DATA = {
        "Player": {"Hp": [10, 10, 30, 2, 50], "Crit %": [1, 1, 5, 1, 50]},
        "Blaster": {"Dmg": [1, 1, 10, 1, 20], "Cooldown": [30, 30, 5, -5, 5],
                    'Range': [60, 60, 90, 10, 10],
                    'Max Ammo': [50, 50, 400, 50, 10]},
        "Shotgun": {"Dmg": [3, 3, 20, 1, 30],
                    "Cooldown": [120, 120, 30, -20, 10],
                    'Range': [20, 20, 40, 10, 20],
                    'Max Ammo': [10, 10, 100, 10, 20]},
        "Rifle": {"Dmg": [20, 20, 200, 10, 40],
                  "Cooldown": [240, 240, 120, -20, 20],
                  'Range': [120, 120, 480, 120, 30],
                  'Max Ammo': [5, 5, 50, 5, 30]},
        "Speed Boost": {"Time": [600, 600, 1200, 100, 40]},
        "Shield": {"Time": [600, 600, 1200, 100, 40]}
    }


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


# sw, sh = screen_info.current_w, screen_info.current_h
sw, sh = 1920, 1080
SW, SH = fit_aspect_ratio(sw, sh)
RATIO = SW / 1920

SONGS = ['stains_of_time', 'metal_shape_synth_ver', 'metal_shape_v2']


def play_sound(filename, volume=0.5):
    sfx = pygame.mixer.Sound(f'assets/sfx/{filename}.wav')
    sfx.set_volume(volume)
    sfx.play()


def play_music(filename, volume=0.5):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(f'assets/music/{filename}.mp3')
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def set_screen(size):
    pygame.display.set_caption('Shape-ish Madness')
    flags = pygame.DOUBLEBUF
    screen = pygame.display.set_mode(size, flags)
    screen_rect = (0, 0, size[0], size[1])
    print(SW, SH)
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
