import pygame


class ExperienceOrb(pygame.sprite.Sprite):
    def __init__(self, pos, image, size, group):
        super().__init__(group)
        self.original_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect()
        self.rect.center = pos

# def spawn_orbs(amount):
#     global total_amount
#     for _ in range(amount):
#         ExperienceOrb((randint(-Settings().map_x, Settings().map_x), randint(-Settings().map_y, Settings().map_y)),
#                       orb_group)
#     total_amount = amount
