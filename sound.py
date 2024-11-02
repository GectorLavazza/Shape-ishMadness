import pygame


class SoundPlayer:
    def __init__(self):
        self.timer = 1
        self.elapsed_time = self.timer
        self.volume = 0.5
        self.music_volume = 0.5
        self.music_set = False
        self.count = 0

    def update(self, dt):
        if self.elapsed_time > 0:
            self.elapsed_time -= dt
        else:
            self.count = 0

        print(self.elapsed_time, self.count)

    def set_music(self, filename):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(f'assets/music/{filename}.mp3')
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)
        self.music_set = True

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def play(self, filename, volume=0):
        if self.volume:
            v = volume
            if not volume:
                v = self.volume

            if self.elapsed_time <= 0 and self.count <= 1:
                sfx = pygame.mixer.Sound(f'assets/sfx/{filename}.wav')
                sfx.set_volume(v)
                sfx.play()
                self.elapsed_time = self.timer
                self.count += 1
