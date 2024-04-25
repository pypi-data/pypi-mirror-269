import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image, size, group):
        super().__init__(group)
        self.original_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 50

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

        # collided_oil = pygame.sprite.spritecollideany(self, oil_group)
        # if collided_oil:
        #     print("Player collided with oil!")
        #     oil_group.remove(collided_oil)
        #     collided_oil.kill()
        #     PlayerStats().oil += 1
        #
        # collided_orb = pygame.sprite.spritecollideany(self, orb_group)
        # if collided_orb:
        #     print("Player collided with orb!")
        #     orb_group.remove(collided_orb)
        #     collided_orb.kill()
        #     global total_amount
        #     total_amount -= 1
        #     PlayerStats().experience += 1
        #
        # keys = pygame.key.get_pressed()
        # if pygame.sprite.spritecollideany(self, rocket_group):
        #     if keys[pygame.K_RETURN]:
        #         if PlayerStats().oil < 5:
        #             print('Not enough')
        #         else:
        #             if PlayerStats().oil == PlayerStats().amount_of_oil:
        #                 print('You win')
        #             else:
        #                 print('You lose')
