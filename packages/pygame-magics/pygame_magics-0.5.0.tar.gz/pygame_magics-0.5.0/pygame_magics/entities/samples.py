def sample_sprite():
    return """
                class Oil(pygame.sprite.Sprite):
                    def __init__(self, pos, group):
                        super().__init__(group)
                        self.original_image = pygame.image.load('graphics/carbons/oil.png').convert_alpha()
                        self.image = pygame.transform.scale(self.original_image, (40, 40))
                        self.rect = self.image.get_rect()
                        self.rect.center = pos
            """


def sample_spawn():
    return """def spawn_orbs(amount):
        global total_amount
        for _ in range(amount):
            ExperienceOrb((randint(-Settings().map_x, Settings().map_x), randint(-Settings().map_y, Settings().map_y)),
                          orb_group)
        total_amount = amount"""


def sample_create():
    return """def create_enemy():
                Enemy(player.rect.center + pygame.math.Vector2(
                    (-1) * randint(1, 2) * screen.get_width() * 1.5,
                    (-1) * randint(1, 2) * screen.get_height() * 1.5), "graphics/ufo/ui2_106.png",
                      (80, 80), 20, 100, enemy_group)
        """


def sample_nearest_enemy():
    """
    uses euclidian distance
    :return:
    """
    return """def get_nearest_enemy():
        arr = []
        for enemy in enemy_group.sprites():
            delta = sqrt((enemy.rect.centerx - player.rect.centerx) ** 2 + (enemy.rect.centery - player.rect.centery) ** 2)
            arr.append((delta, enemy))
        return min(arr, key=lambda x: x[0])[1] if arr else 0"""


def sample_check_collide():
    return """
                collided_oil = pygame.sprite.spritecollideany(self, oil_group)
                if collided_oil:
                    print("Player collided with oil!")
                    oil_group.remove(collided_oil)
                    collided_oil.kill()
                    PlayerStats().oil += 1
            """


def sample_delays():
    return """
                current_time = pygame.time.get_ticks()
                if current_time - enemy_timer > ENEMY_SPAWN_INTERVAL * (SPAWN_COEFFICIENT ** (current_time // 1000)):
                    create_enemy()
                    enemy_timer = current_time
                if current_time - magic_bolt_timer > MAGIC_BOLT_SPAWN_INTERVAL:
                    magic_bolt.update(player.rect.center, magic_bolt_group)
                    magic_bolt_timer = current_time
                if current_time - magic_bolt_timer > MAGIC_BOLT_FIRE_INTERVAL:
                    magic_bolt.stop_fire(magic_bolt_group, enemy_group)
                    magic_bolt_group.update(magic_bolt_group)
            """


def sample_event_cycle():
    return """    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        if total_amount < normal_amount // 2:
            spawn_orbs(normal_amount)
        pygame.display.update()
        clock.tick(60)"""


def sample_configs():
    return """
            normal_amount = 400
            enemy_timer = 0
            magic_bolt_timer = 0
            ENEMY_SPAWN_INTERVAL = 3000
            SPAWN_COEFFICIENT = 0.997
            
            MAGIC_BOLT_SPAWN_INTERVAL = 1000
            MAGIC_BOLT_FIRE_INTERVAL = 1000
            
            MAGIC_BOLT_FIRE_SPEED = 200
            
            spawn_orbs(normal_amount)
            """
