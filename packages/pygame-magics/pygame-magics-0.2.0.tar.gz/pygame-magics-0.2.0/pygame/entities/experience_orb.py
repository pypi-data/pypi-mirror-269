import pygame


class ExperienceOrb(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.original_image = pygame.image.load('graphics/experience_orb/experience.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = pos
