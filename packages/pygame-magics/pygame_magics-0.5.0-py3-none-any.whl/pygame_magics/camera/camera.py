import pygame


class CameraGroup(pygame.sprite.Group):

    def __init__(self, map_x, map_y, field_img, size_coefficient=1):
        """
            https://github.com/clear-code-projects/Pygame-Cameras
            https://www.youtube.com/watch?v=u7LPRqrzry8
            :param map_x: map width
            :param map_y: map height
            :param field_img: image of a map
            :param size_coefficient: coefficient of resizing
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.ground_surf = pygame.image.load(field_img)
        self.ground_surf = pygame.transform.scale(self.ground_surf, (self.ground_surf.get_width() * size_coefficient,
                                                                     self.ground_surf.get_height() * size_coefficient))
        self.ground_rect = self.ground_surf.get_rect(topleft=(-map_x, -map_y))

        self.map_x = map_x
        self.map_y = map_y

        self.offset = pygame.math.Vector2(800, 300)
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_target_camera(self, target):
        """
        it centralizes player on camera
        :param target: player
        :return:
        """
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def round_walk_effect(self, target):
        """
        it makes that player goes round
        :param target: player
        :return:
        """
        min_x = self.offset.x - self.half_w
        max_x = self.offset.x + self.half_w
        min_y = self.offset.y - self.half_h
        max_y = self.offset.y + self.half_h

        if target.rect.right < min_x:
            target.rect.right = min_x
        elif target.rect.left > max_x:
            target.rect.left = max_x
        if target.rect.bottom < min_y:
            target.rect.bottom = min_y
        elif target.rect.top > max_y:
            target.rect.top = max_y

        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

        if self.offset.x < -self.map_x:
            self.offset.x = -self.map_x
        elif self.offset.x > self.map_x:
            self.offset.x = self.map_x
        if self.offset.y < -self.map_y:
            self.offset.y = -self.map_y
        elif self.offset.y > self.map_y:
            self.offset.y = self.map_y

    def map_draw(self):
        """
        draw map
        :return:
        """
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

    def custom_draw(self, *args):
        """
        the most important function where it mest ne sprite group to be shown
        :param args: group sprites
        :return:
        """
        player = args[0]
        groups = args[1:]

        self.map_draw()

        self.center_target_camera(player)
        self.round_walk_effect(player)

        all_sprites = []
        for group in groups:
            all_sprites.extend(group.sprites())
        all_sprites.append(player)

        for sprite in sorted(all_sprites, key=lambda x: x.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
