import pygame

pygame.display.init()
screen_info = pygame.display.Info()
SW, SH = screen_info.current_w, screen_info.current_h
# SW, SH = 800, 800


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
    pygame.display.set_caption('Shapish Madness')
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, size[0], size[1])

    return screen, size, screen_rect
