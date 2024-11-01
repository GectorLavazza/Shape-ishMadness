import random

from pygame import Vector2

from bullets import create_bullet
from load_image import load_image
from particles import create_particles, generate_particles
from settings import *
from sprites import Sprite


class Player(Sprite):
    def __init__(self, bullets_g, particles_g, enemy_bullet_g, data, *group):
        super().__init__(*group)
        self.image = load_image('player')

        self.rect = self.image.get_rect()
        self.rect.center = SW // 2, SH // 2
        self.hitbox = pygame.Rect(0, 0, self.rect.w * 0.72, self.rect.h * 0.72)
        self.hitbox.topleft = (
            self.rect.centerx + -self.hitbox.w // 2,
            self.rect.centery + -self.hitbox.h // 2)

        self.dx = 0
        self.dy = 0

        self.speed = 5
        self.max_speed = 8
        self.acceleration = 0.5
        self.deceleration = 0.1
        self.velocity = pygame.Vector2(0, 0)  # Current velocity

        self.data = data.data

        self.score = 100000
        self.coins = 0
        self.health = self.data['Player']['Hp'][0]
        self.max_health = self.data['Player']['Hp'][0]
        self.crit_chance = self.data['Player']['Crit %'][0]

        self.hold = False
        self.cooldown = 0
        self.hold_mode = False
        self.sprint = False

        self.speed_boost_timer = self.data['Spd Boost']['Time'][0]
        self.shield_timer = self.data['Shield']['Time'][0]
        self.max_speed_boost_time = self.data['Spd Boost']['Time'][0]
        self.max_shield_time = self.data['Shield']['Time'][0]
        self.magnet_timer = self.data['Magnet']['Time'][0]
        self.max_magnet_time = self.data['Magnet']['Time'][0]

        self.magnet = False
        self.speed_boost = 0
        self.shield = False

        self.bullets_g = bullets_g
        self.particles_g = particles_g
        self.enemy_bullet_g = enemy_bullet_g

        self.blaster = self.data['Blaster']
        self.blaster_plus = self.data['Blaster+']

        self.sprint_speed = 8
        self.normal_speed = 5

        self.ammo = self.blaster['Max Ammo'][0]


    def update(self, screen, screen_rect, dt):
        self.move(dt)
        self.bullet_check()
        self.handle_sprint()
        self.handle_timers(screen, dt)


    def take_damage(self, damage):
        if not self.shield:
            self.health -= damage
            play_sound('hit')
            create_particles(self.rect.center,
                             generate_particles('hit_particle'),
                             50, 20,
                             self.particles_g)
        else:
            self.health -= int(damage * 0.1)
            play_sound('shield_hit')
            create_particles(self.rect.center,
                             generate_particles('shield_hit_particle'),
                             50, 20,
                             self.particles_g)

    def shoot(self, mouse_pos):
        damage = self.blaster['Dmg'][0]

        if random.randint(1, 10) in range(1, self.crit_chance + 1):
            damage *= 2

        c_time = self.blaster['Cooldown'][0]
        e_time = self.blaster_plus['Range'][0]

        if self.cooldown >= c_time and self.ammo:
            play_sound('shoot2', 0.2)

            spread_angle = self.blaster_plus['Angle'][0]
            num_bullets = self.blaster_plus['Amount'][0]

            direction = Vector2(mouse_pos) - Vector2(self.rect.center)
            distance = direction.length()
            if distance > 0:
                direction = direction.normalize()
            if num_bullets > 1:
                for i in range(num_bullets):
                    angle_offset = spread_angle * (i / (num_bullets - 1) - 0.5)
                    rotated_direction = direction.rotate(angle_offset)

                    target = Vector2(
                        self.rect.center) + rotated_direction * distance


                    create_bullet(self.rect.center, target,
                                  damage, e_time,
                                  self.particles_g, self.bullets_g)
            else:
                create_bullet(self.rect.center, mouse_pos,
                              damage, e_time,
                              self.particles_g, self.bullets_g)

            self.cooldown = 0

            self.ammo -= 1

    def draw_cooldown_bar(self, screen, cooldown):
        c_time = self.blaster['Cooldown'][0]
        pygame.draw.rect(screen, pygame.Color('#306230'),
                         pygame.Rect(self.rect.centerx - 15 * RATIO, self.rect.y - 10 * RATIO,
                                     30 * RATIO, 5 * RATIO))
        pygame.draw.rect(screen, pygame.Color('#8bac0f'),
                         pygame.Rect(self.rect.centerx - 15 * RATIO, self.rect.y - 10 * RATIO,
                                     30 / c_time * cooldown * RATIO, 5 * RATIO))

    def draw_shield(self, screen):
        image = load_image('shield_cover')
        screen.blit(image, (self.rect.centerx - image.get_width() // 2,
                            self.rect.centery - image.get_height() // 2))

    def move(self, dt):
        input_direction = pygame.Vector2(self.dx, self.dy)

        if input_direction.length() > 0:
            input_direction = input_direction.normalize()

            # Accelerate towards input direction
            self.velocity.x += input_direction.x * self.acceleration * dt * RATIO
            self.velocity.y += input_direction.y * self.acceleration * dt * RATIO
        else:
            # Decelerate when no input
            if self.velocity.length() > 0:
                self.velocity.x -= self.velocity.x * self.deceleration * dt * RATIO
                self.velocity.y -= self.velocity.y * self.deceleration * dt * RATIO

        # Cap velocity to max speed
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # Update player position based on velocity
        if 0 <= self.rect.x + self.velocity.x * dt * RATIO <= SW - self.rect.w:
            self.rect.centerx += self.velocity.x * dt * RATIO
            self.hitbox.centerx += self.velocity.x * dt * RATIO
        if 0 <= self.rect.y + self.velocity.y * dt * RATIO <= SH - self.rect.h:
            self.rect.centery += self.velocity.y * dt * RATIO
            self.hitbox.centery += self.velocity.y * dt * RATIO

    def handle_sprint(self):
        if not self.hold:
            if self.sprint:
                self.max_speed = self.sprint_speed + self.speed_boost
            else:
                self.max_speed = self.normal_speed + self.speed_boost
        else:
            self.max_speed = self.normal_speed + self.speed_boost

    def bullet_check(self):
        for bullet in self.enemy_bullet_g:
            if self.hitbox.colliderect(bullet.rect):
                self.take_damage(1)
                bullet.kill()

    def handle_timers(self, screen, dt):
        c_time = self.blaster['Cooldown'][0]
        if self.cooldown < c_time:
            self.cooldown += dt
            self.draw_cooldown_bar(screen, self.cooldown)

        if self.speed_boost_timer > 0 and self.speed_boost:
            self.speed_boost_timer -= dt
        else:
            self.speed_boost = 0

        if self.shield_timer > 0 and self.shield:
            self.shield_timer -= dt
            self.draw_shield(screen)
        else:
            self.shield = False

        if self.magnet_timer > 0 and self.magnet:
            self.magnet_timer -= dt
        else:
            self.magnet = False

    def update_stats(self, data, menu):
        self.data = data.data
        ch, cn = menu.current_heading, menu.current_name

        self.max_health = self.data['Player']['Hp'][0]
        if ch == 'Player' and cn == 'Hp':
            self.health = self.max_health

        self.crit_chance = self.data['Player']['Crit %'][0]

        self.max_speed_boost_time = self.data['Spd Boost']['Time'][0]
        self.max_shield_time = self.data['Shield']['Time'][0]

        self.blaster = self.data['Blaster']

        if ch == 'Blaster' and cn == 'Max Ammo':
            self.ammo = self.data[ch]['Max Ammo'][0]
