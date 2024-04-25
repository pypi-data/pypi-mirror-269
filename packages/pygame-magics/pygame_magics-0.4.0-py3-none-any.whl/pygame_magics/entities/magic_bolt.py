from math import degrees, cos, sin, atan2

import pygame


class MagicBoltBullet(pygame.sprite.Sprite):
    def __init__(self, pos, image, angle, damage, size, speed, delay, group):
        super().__init__(group)
        self.original_image = (pygame.image.load(image).
                               convert_alpha())
        orig_size = self.original_image.get_size()
        self.image = pygame.transform.scale(pygame.transform.rotate(self.original_image, degrees(angle)),
                                            (orig_size[0] * size, orig_size[1] * size))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = angle
        self.damage = damage
        self.velocity = speed
        self.t = 0
        self.delay = delay

    def update(self, enemies):
        if self.delay <= self.t:
            self.rect.centerx = self.rect.centerx + self.velocity * self.t * cos(-self.angle)
            self.rect.centery = self.rect.centery - self.velocity * self.t * sin(self.angle)
        self.t += 1

        for enemy in enemies.sprites():
            if pygame.sprite.collide_rect(self, enemy):
                enemy.lost_hp(self.damage)
                if enemy.hp <= 0:
                    enemy.remove()
                    enemy.kill()


class MagicBolt:
    def __init__(self, player_pos):
        self.player_pos = player_pos

    def spawn_magic_bolt(self, magic_bolt_group, player, n, nearest_enemy_func):
        amount = 1
        damage = 10
        size = 1
        speed = 1
        if n >= 2:
            amount += 1
        if n >= 3:
            damage = damage * 1.3
        if n >= 4:
            damage = damage * 1.8
            size = 1.8 * size
            speed = 1.8 * speed
        if n >= 5:
            amount += 1
        if n >= 6:
            damage = damage * 1.5
        if n >= 7:
            damage = damage * 1.7
            size = 1.5 * size
        for j in range(amount):
            enemy_rect = nearest_enemy_func()
            if enemy_rect:
                enemy_rect = enemy_rect.rect.center
                player_rect = player.rect.center
                angle = atan2((enemy_rect[1] - player_rect[1]), (enemy_rect[0] - player_rect[0]))
                delay = 20 * j
                MagicBoltBullet(self.player_pos, angle, damage, size, speed, delay, magic_bolt_group)

    def stop_fire(self, magic_bolt_group, enemies):
        for sprite in magic_bolt_group.sprites():
            sprite.remove()
            sprite.kill()
            sprite.update(enemies)

    def update(self, player_position, magic_bolt_group):
        self.player_pos = player_position
        self.spawn_magic_bolt(magic_bolt_group)


# def create_enemy():
#     Enemy(player.rect.center + pygame.math.Vector2(
#         (-1) * randint(1, 2) * screen.get_width() * 1.5,
#         (-1) * randint(1, 2) * screen.get_height() * 1.5), enemy_group)


# def get_nearest_enemy():
#     arr = []
#     for enemy in enemy_group.sprites():
#         delta = sqrt((enemy.rect.centerx - player.rect.centerx) ** 2 + (enemy.rect.centery - player.rect.centery) ** 2)
#         arr.append((delta, enemy))
#     return min(arr, key=lambda x: x[0])[1] if arr else 0