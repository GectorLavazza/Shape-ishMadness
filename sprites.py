import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
