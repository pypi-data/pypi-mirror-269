import pygame_magics


class Enemy(pygame_magics.sprite.Sprite):
    def __init__(self, pos, image, image_size, speed, health, group):
        super().__init__(group)
        self.original_image = pygame_magics.image.load(image).convert_alpha()
        self.image = pygame_magics.transform.scale(self.original_image, image_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = speed
        self.hp = health

    def lost_hp(self, amount_hp):
        self.hp -= amount_hp

    def update(self, player):
        direction_vector = pygame_magics.math.Vector2(player.rect.center) - pygame_magics.math.Vector2(self.rect.center)
        direction_vector.normalize_ip()
        self.rect.move_ip(direction_vector * self.speed)
        # if pygame_magics.sprite.collide_rect(self, player):
        #     PlayerStats().health -= 1
