# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
#
# camera_group = pygame.camera.camera.CameraGroup(Settings().map_x, Settings().map_y, 'graphics/mars_photogrammetry/map.png', 12)
#
# player = Player((640, 360), camera_group)
# PlayerStats().player = player
#
# oil_group = pygame.sprite.Group()
# orb_group = pygame.sprite.Group()
# rocket_group = pygame.sprite.Group()
# enemy_group = pygame.sprite.Group()
# magic_bolt_group = pygame.sprite.Group()
#
# magic_bolt = MagicBolt(player.rect.center)
# amount_of_oil = randint(5, 9)
# PlayerStats().amount_of_oil = amount_of_oil
# for i in range(amount_of_oil):
#     random_x = randint(-Settings().map_x, Settings().map_x)
#     random_y = randint(-Settings().map_y, Settings().map_y)
#     Oil((random_x, random_y), oil_group)
#
# Rocket((0, 0), rocket_group)
#
# total_amount = 0
#
# normal_amount = 400
# enemy_timer = 0
# magic_bolt_timer = 0
# ENEMY_SPAWN_INTERVAL = 3000
# SPAWN_COEFFICIENT = 0.997
#
# MAGIC_BOLT_SPAWN_INTERVAL = 1000
# MAGIC_BOLT_FIRE_INTERVAL = 1000
#
# MAGIC_BOLT_FIRE_SPEED = 200
#
# spawn_orbs(normal_amount)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()
#
#     screen.fill('#71ddee')
#     camera_group.update(oil_group, orb_group, rocket_group)
#     current_time = pygame.time.get_ticks()
#     if current_time - enemy_timer > ENEMY_SPAWN_INTERVAL * (SPAWN_COEFFICIENT ** (current_time // 1000)):
#         create_enemy()
#         enemy_timer = current_time
#     camera_group.custom_draw(player, oil_group, orb_group, rocket_group, enemy_group, magic_bolt_group)
#     enemy_group.update(player)
#     orb_group.update()
#     oil_group.update()
#     magic_bolt_group.update(enemy_group)
#     if PlayerStats().health <= 0:
#         break
#     PlayerStats().check_experience()
#     if current_time - magic_bolt_timer > MAGIC_BOLT_SPAWN_INTERVAL:
#         magic_bolt.update(player.rect.center, magic_bolt_group)
#         magic_bolt_timer = current_time
#     if current_time - magic_bolt_timer > MAGIC_BOLT_FIRE_INTERVAL:
#         magic_bolt.stop_fire(magic_bolt_group, enemy_group)
#         magic_bolt_group.update(magic_bolt_group)
#     pygame.display.flip()
#     if total_amount < normal_amount // 2:
#         spawn_orbs(normal_amount)
#     pygame.display.update()
#     clock.tick(60)
# class Settings(metaclass=Singleton):
#
#     def __init__(self):
#         self.map_x = 2800 * 3
#         self.map_y = 1300 * 3
#
#
# class PlayerStats(metaclass=Singleton):
#
#     def __init__(self):
#         self.health = 100
#         self.player = None
#         self.experience = 0
#         self.n = 1
#         self.oil = 0
#         self.amount_of_oil = 0
