from bullets import create_enemy_bullet
from items import *
from settings import *


class Triangle(Sprite):
    def __init__(self, pos, particles_g, bullet_g, items_g, player, *group):
        super().__init__(*group)

        self.image = load_image('triangle')
        self.name = 'triangle'
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.hitbox = pygame.Rect(0, 0, self.rect.w // 2, self.rect.h // 2)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)

        self.particles_g = particles_g
        self.bullet_g = bullet_g
        self.player = player
        self.items_g = items_g
        self.all_enemies = group[0]

        self.elapsed_time = 0

        self.quotient = (5 + self.player.score // 50 -
                         3 * self.player.score // 200 -
                         3 * self.player.score // 1000 -
                         3 * self.player.score // 2000 -
                         2 * self.player.score // 5000 -
                         1 * self.player.score // 10000) / 10
        if self.quotient > 1:
            self.quotient = 1

        self.max_speed = int(random.choices(range(4, 9),
                                            weights=(1, 2, 3, 2, 1), k=1)[0] *
                             self.quotient)
        if self.max_speed < 4:
            self.max_speed = 4

        self.max_health = 2 + self.player.score // 2000
        self.health = 2 + self.player.score // 2000
        self.damage = 1 + self.player.score // 3000
        self.score_weight = 5
        self.dx = 0
        self.dy = 0

        self.damage_timer = 0

        self.acceleration = 0.7
        self.deceleration = 0.3
        self.velocity = pygame.Vector2(0, 0)
        self.recovering = False  # Track if the enemy is recovering after the hit
        self.push_strength = 0.5

    def update(self, screen, screen_rect, target_pos, dt):
        self.move(target_pos, dt)
        if (0 <= self.rect.centerx <= SW and
                0 <= self.rect.centery <= SH):
            self.bullet_check()
            self.player_check()
        self.draw_health_bar(screen)
        self.handle_overlap(self.all_enemies, dt)

        # Handle damage cooldown and recovery
        if self.damage_timer < 120:
            self.damage_timer += dt
            self.recovering = True
        else:
            self.recovering = False  # Stop recovering when cooldown is done

    def handle_overlap(self, all_enemies, dt):
        for other in all_enemies:
            if other != self and self.rect.colliderect(other.rect):
                # Calculate the push direction
                push_direction = pygame.Vector2(
                    self.rect.center) - pygame.Vector2(other.rect.center)

                # Normalize to avoid scaling with distance, then apply push strength
                if push_direction.length() > 0:
                    push_direction = push_direction.normalize()

                # Apply a small force to each enemy to separate them
                self.velocity += push_direction * self.push_strength * dt * RATIO
                other.velocity -= push_direction * self.push_strength * dt * RATIO

    def move(self, target_pos, dt):
        direction = pygame.Vector2(target_pos) - pygame.Vector2(
            self.rect.center)

        if direction.length() > 0:
            direction = direction.normalize()

            # If recovering (after hitting the player), decelerate
            if self.recovering:
                self.velocity.x -= self.velocity.x * self.deceleration * 0.5 * dt * RATIO
                self.velocity.y -= self.velocity.y * self.deceleration * 0.5 * dt * RATIO
            else:
                # Normal acceleration towards the target
                self.velocity.x += direction.x * self.acceleration * dt * RATIO
                self.velocity.y += direction.y * self.acceleration * dt * RATIO
        else:
            # Decelerate when no input
            if self.velocity.length() > 0:
                self.velocity.x -= self.velocity.x * self.deceleration * dt * RATIO
                self.velocity.y -= self.velocity.y * self.deceleration * dt * RATIO

        # Cap velocity to max speed
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # Update position based on velocity
        self.rect.centerx += self.velocity.x * dt * RATIO
        self.hitbox.centerx += self.velocity.x * dt * RATIO
        self.rect.centery += self.velocity.y * dt * RATIO
        self.hitbox.centery += self.velocity.y * dt * RATIO

    def bullet_check(self):
        for bullet in self.bullet_g:
            if self.rect.colliderect(bullet.rect):

                self.health -= bullet.damage

                bullet.kill()
                if self.health > 0:
                    self.take_damage()
                else:
                    self.death()

    def generate_coin(self, pos):
        coin = Coin(self.player, pos,
                    self.particles_g, self.items_g)
        self.items_g.add(coin)

    def generate_item(self, item_type, pos):
        if item_type == 'health':
            item = HealthBox(self.player, pos,
                             2, self.particles_g, self.items_g)
        if item_type == 'ammo':
            item = AmmoBox(self.player, pos, self.particles_g, self.items_g)
        if item_type == 'speed':
            item = SpeedBoost(self.player, pos,
                              self.particles_g, self.items_g)
        if item_type == 'shield':
            item = Shield(self.player, pos,
                          self.particles_g, self.items_g)
        self.items_g.add(item)

    def death(self):
        self.player.score += self.score_weight

        play_sound('explosion')
        create_particles(self.rect.center,
                         generate_particles('death_particle'),
                         50, 30,
                         self.particles_g)

        item_type = random.choices(['health', 'ammo', 'speed', 'shield', ''],
                                   weights=(1, 2, 2, 1, 17), k=1)[0]
        # weights=(1, 2, 2, 1, 17)
        if item_type:
            pos = (self.rect.centerx + random.randint(0, 10),
                   self.rect.centery + random.randint(0, 10))
            self.generate_item(item_type, pos)
        else:
            pos = (self.rect.centerx + random.randint(0, 10),
                   self.rect.centery + random.randint(0, 10))
            self.generate_coin(pos)

        self.kill()

    def player_check(self):
        if self.damage_timer >= 120:
            if self.hitbox.colliderect(self.player.hitbox):
                self.player.take_damage(self.damage)
                self.damage_timer = 0
                self.recovering = True
                if (not self.player.ammo and
                        not len(list(filter(lambda s: type(s) == AmmoBox,
                                            self.items_g)))):
                    pos = (self.rect.centerx + random.randint(0, 10),
                           self.rect.centery + random.randint(0, 10))
                    self.generate_item('ammo', pos)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, pygame.Color('#306230'),
                         pygame.Rect(self.rect.centerx - 15 * RATIO,
                                     self.rect.y - 10 * RATIO,
                                     30 * RATIO, 5 * RATIO))
        pygame.draw.rect(screen, pygame.Color('#8bac0f'),
                         pygame.Rect(self.rect.centerx - 15 * RATIO,
                                     self.rect.y - 10 * RATIO,
                                     30 / self.max_health * self.health * RATIO,
                                     5 * RATIO))

    def take_damage(self):
        play_sound('enemy_hit')
        create_particles(self.rect.center,
                         generate_particles(
                             f'{self.name}_particle'),
                         30, 15,
                         self.particles_g)


class Square(Triangle):
    def __init__(self, pos, particles_g, bullet_g, items_g, player, *group):
        super().__init__(pos, particles_g, bullet_g, items_g, player, *group)

        self.image = load_image('square')
        self.name = 'square'
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.hitbox = pygame.Rect(0, 0, self.rect.w - 10, self.rect.h - 10)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)

        self.max_speed = int(random.choices(range(2, 7),
                                            weights=(3, 3, 2, 2, 1), k=1)[0] *
                             self.quotient)

        if self.max_speed < 2:
            self.max_speed = 2

        self.max_health = 4 + 1 * self.player.score // 2000
        self.health = 4 + 1 * self.player.score // 2000
        self.damage = 2 + self.player.score // 3000

        self.score_weight = 10

        self.acceleration = 0.1
        self.deceleration = 0.05


class Pentagon(Triangle):
    def __init__(self, pos, particles_g, bullet_g, items_g, enemy_bullet_g,
                 player, *group):
        super().__init__(pos, particles_g, bullet_g, items_g, player, *group)
        self.image = load_image('pentagon')
        self.name = 'pentagon'
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.hitbox = pygame.Rect(0, 0, self.rect.w - 40, self.rect.h - 40)
        self.hitbox.topleft = (
            self.rect.centerx + - self.hitbox.w // 2,
            self.rect.centery + - self.hitbox.h // 2)

        self.max_speed = 1
        self.health = 100 + 20 * self.player.score // 2000
        self.max_health = 100 + 20 * self.player.score // 2000
        self.damage = 5 + self.player.score // 5000
        self.score_weight = 100

        self.enemy_bullet_g = enemy_bullet_g

        self.acceleration = 0.025
        self.deceleration = 0.0125

        self.cooldown = 0
        self.c_time = 60 - 2 * self.player.score // 2000
        if self.c_time < 30:
            self.c_time = 30

    def update(self, screen, screen_rect, target_pos, dt):
        self.move(target_pos, dt)
        if (0 <= self.rect.centerx <= SW and
                0 <= self.rect.centery <= SH):
            self.bullet_check()
            self.player_check()
        self.draw_health_bar(screen)
        self.handle_overlap(self.all_enemies, dt)

        if self.damage_timer < 120:
            self.damage_timer += dt
            self.recovering = True
        else:
            self.recovering = False

        if self.cooldown < self.c_time:
            self.cooldown += dt

        self.shoot()

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, pygame.Color('#306230'),
                         pygame.Rect(self.rect.centerx - 30, self.rect.y - 10,
                                     60, 5))
        pygame.draw.rect(screen, pygame.Color('#8bac0f'),
                         pygame.Rect(self.rect.centerx - 30, self.rect.y - 10,
                                     60 / self.max_health * self.health, 5))

    def bullet_check(self):
        for bullet in self.bullet_g:
            if self.hitbox.colliderect(bullet.rect):
                self.health -= bullet.damage
                bullet.kill()
                if self.health > 0:
                    self.take_damage()
                else:
                    self.death()
                    self.kill()

    def shoot(self):
        if self.cooldown >= self.c_time:
            play_sound('enemy_bullet', 0.2)
            create_enemy_bullet(self.rect.center, self.player.rect.center,
                                self.particles_g, self.enemy_bullet_g)
            self.cooldown = 0

    def death(self):
        self.player.score += self.score_weight

        play_sound('explosion')
        create_particles(self.rect.center,
                         generate_particles('death_particle'),
                         80, 60,
                         self.particles_g)

        for i in range(random.randint(3, 6)):
            item_type = \
                random.choices(['health', 'ammo', 'speed', 'shield'],
                               weights=(2, 3, 1, 1), k=1)[0]
            pos = (self.rect.centerx + random.randint(0, 100),
                   self.rect.centery + random.randint(0, 100))
            self.generate_item(item_type, pos)

        for i in range(random.randint(10, 20)):
            pos = (self.rect.centerx + random.randint(0, 100),
                   self.rect.centery + random.randint(0, 100))
            self.generate_coin(pos)

        self.kill()

    def take_damage(self):
        play_sound('enemy_hit')
        create_particles(self.rect.center,
                         generate_particles(
                             f'{self.name}_particle'),
                         40, 30,
                         self.particles_g)


class EnemySpawn:
    def __init__(self, group, particles_g, bullet_g, items_g, enemy_bullet_g,
                 player):
        self.elapsed_time = 0
        self.spawn_time = 5
        self.group = group
        self.particles_g = particles_g
        self.bullet_g = bullet_g
        self.player = player
        self.items_g = items_g
        self.enemy_bullet_g = enemy_bullet_g
        self.pentagon_count = 0
        self.score = 0
        self.max_enemy_count = 5

        self.x = range(-400, SW + 400, 100)
        self.y = range(-400, SH + 400, 100)

    def update(self, dt):
        self.elapsed_time += dt

        self.score = self.player.score
        self.max_enemy_count = (5 + self.player.score // 20 -
                                3 * self.player.score // 100 -
                                2 * self.player.score // 200 -
                                2 * self.player.score // 1000 -
                                7 * self.player.score // 2000)

        if self.elapsed_time >= self.spawn_time and len(
                self.group) <= self.max_enemy_count:
            self.elapsed_time = 0

            pos = random.choice(self.x), random.choice(self.y)
            if not (-200 <= pos[0] <= SW + 200 and -200 <= pos[1] <= SH + 200):
                enemy_type = \
                    random.choices(['square', 'triangle', 'pentagon'],
                                   weights=(3, 7, 1), k=1)[0]

                self.generate_enemy(pos, enemy_type)

    def generate_enemy(self, pos, enemy_type):
        if enemy_type == 'square':
            enemy = Square(pos, self.particles_g, self.bullet_g,
                           self.items_g,
                           self.player, self.group)
            self.group.add(enemy)
        elif enemy_type == 'triangle':
            enemy = Triangle(pos, self.particles_g, self.bullet_g,
                             self.items_g,
                             self.player, self.group)
            self.group.add(enemy)
        else:
            if self.score > 200:
                m = 1 + self.score // 4000
                if [e.name == 'pentagon' for e in self.group].count(True) < m:
                    enemy = Pentagon(pos, self.particles_g, self.bullet_g,
                                     self.items_g, self.enemy_bullet_g,
                                     self.player, self.group)

                    self.group.add(enemy)
