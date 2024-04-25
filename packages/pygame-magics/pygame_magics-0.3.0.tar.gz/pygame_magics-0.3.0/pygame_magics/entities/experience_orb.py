import pygame_magics


class ExperienceOrb(pygame_magics.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.original_image = pygame_magics.image.load('graphics/experience_orb/experience.png').convert_alpha()
        self.image = pygame_magics.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = pos
