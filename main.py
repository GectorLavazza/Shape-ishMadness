import asyncio
import time

import pygame

from cursor import Cursor
from enemies import *
from player import Player
from ui import *


async def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen, size, screen_rect = set_screen((SW, SH))
    pygame.event.set_allowed([pygame.QUIT,
                              pygame.KEYDOWN,
                              pygame.KEYUP,
                              pygame.MOUSEBUTTONDOWN,
                              pygame.MOUSEBUTTONUP,
                              pygame.MOUSEWHEEL])
    pygame.mouse.set_visible(False)

    last_time = time.time()

    running = True

    d = {
        "Player": {"Hp": [30, 10, 30, 2, 50],
                   "Crit %": [5, 1, 5, 1, 50]},
        "Blaster": {"Dmg": [10, 1, 10, 1, 20],
                    "Cooldown": [5, 30, 5, -5, 5],
                    'Max Ammo': [1000, 50, 1000, 50, 10]},
        'Blaster+': {'Range': [240, 60, 240, 10, 10],
                      'Amount': [21, 1, 21, 2, 30],
                      'Angle': [90, 10, 90, 10, 50]},
        "Spd Boost": {"Time": [1200, 600, 1200, 100, 40]},
        "Shield": {"Time": [1200, 600, 1200, 100, 40]},
        "Magnet": {"Time": [600, 300, 600, 100, 40]}
    }

    data = Data(d)

    particles_g = pygame.sprite.Group()
    bullets_g = pygame.sprite.Group()
    enemies_g = pygame.sprite.Group()
    items_g = pygame.sprite.Group()
    enemy_bullet_g = pygame.sprite.Group()
    cursor_g = pygame.sprite.Group()

    cursor = Cursor(cursor_g)

    player_g = pygame.sprite.Group()
    player = Player(bullets_g, particles_g, enemy_bullet_g, data, player_g)

    enemy_spawn = EnemySpawn(enemies_g, particles_g, bullets_g, items_g,
                             enemy_bullet_g, player)

    score_label = Text(screen, size, 40, pos=(SW // 2, 25))

    health = ValueBar(screen, size, player.max_health, 'heart', (10, 10))

    ammo = ValueBar(screen, size, 20, 'ammo', (10, 50))

    speed_boost_bar = ValueBar(screen, size, player.max_speed_boost_time,
                               'speed_boost', (10, 0))
    shield_bar = ValueBar(screen, size, player.max_speed_boost_time, 'shield',
                          (10, 0))
    magnet_bar = ValueBar(screen, size, player.max_magnet_time, 'magnet',
                          (10, 0))

    fps_label = Text(screen, size, 10, pos=(40, SH - 15))

    hint_label = Text(screen, size, 12, pos=(SW // 2, SH - 15))

    pause_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))
    dead_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))

    coin_label = CoinsCount(screen, size, 30, 'white', pos=(SW - 50, 10))

    menu = UpgradesMenu(screen, (SW, SH), data, player)

    # play_music(SONGS[0], 0.3)

    show_hint = True
    show_hitbox = False
    show_rect = False

    playing = True
    show_menu = False

    while running:

        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_q:
                #     if not playing:
                #         running = False

                if event.key == pygame.K_r:
                    if player.health <= 0:
                        playing = True

                        particles_g = pygame.sprite.Group()
                        bullets_g = pygame.sprite.Group()
                        enemies_g = pygame.sprite.Group()
                        items_g = pygame.sprite.Group()
                        enemy_bullet_g = pygame.sprite.Group()

                        player_g = pygame.sprite.Group()

                        d = {
                            "Player": {"Hp": [30, 10, 30, 2, 50],
                                       "Crit %": [5, 1, 5, 1, 50]},
                            "Blaster": {"Dmg": [10, 1, 10, 1, 20],
                                        "Cooldown": [5, 30, 5, -5, 5],
                                        'Max Ammo': [1000, 50, 1000, 50, 10]},
                            'Blaster+': {'Range': [240, 60, 240, 10, 10],
                                          'Amount': [21, 1, 21, 2, 30],
                                          'Angle': [90, 10, 90, 10, 50]},
                            "Spd Boost": {
                                "Time": [1200, 600, 1200, 100, 40]},
                            "Shield": {"Time": [1200, 600, 1200, 100, 40]},
                            "Magnet": {"Time": [600, 300, 600, 100, 40]}
                        }

                        data = Data(d)
                        player = Player(bullets_g, particles_g, enemy_bullet_g,
                                        data, player_g)
                        menu = UpgradesMenu(screen, (SW, SH), data, player)

                        enemy_spawn = EnemySpawn(enemies_g, particles_g,
                                                 bullets_g,
                                                 items_g, enemy_bullet_g,
                                                 player)

                if event.key == pygame.K_ESCAPE:
                    if player.health and not show_menu:
                        playing = not playing

                if event.key == pygame.K_e:
                    if player.health and playing:
                        show_menu = not show_menu

                # if event.key == pygame.K_F1:
                #     if fps == 120:
                #         fps = 60
                #     elif fps == 60:
                #         fps = 10
                #     elif fps == 10:
                #         fps = 120

                if event.key == pygame.K_F2:
                    show_hint = not show_hint

                if event.key == pygame.K_F3:
                    show_hitbox = not show_hitbox

                if event.key == pygame.K_F4:
                    show_rect = not show_rect

                if event.key == pygame.K_LSHIFT:
                    player.sprint = True

                if not show_menu:
                    if event.key == pygame.K_w:
                        player.dy = -1
                    if event.key == pygame.K_s:
                        player.dy = 1
                    if event.key == pygame.K_a:
                        player.dx = -1
                    if event.key == pygame.K_d:
                        player.dx = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.dy = 0
                if event.key == pygame.K_s:
                    player.dy = 0
                if event.key == pygame.K_a:
                    player.dx = 0
                if event.key == pygame.K_d:
                    player.dx = 0

                if event.key == pygame.K_LSHIFT:
                    player.sprint = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    player.hold = True

                elif event.button == 1:
                    if playing and not show_menu:
                        player.shoot(mouse_pos)

                if show_menu:
                    if event.button == 1:
                        try:
                            menu.buy()
                            player.update_stats(data, menu)
                            health.max = player.max_health
                            shield_bar.max = player.max_shield_time
                            speed_boost_bar.max = player.max_speed_boost_time
                        except Exception as e:
                            print(e)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    player.hold = False

        if playing and not show_menu:
            if player.hold:
                player.shoot(mouse_pos)

        if player.health <= 0:
            playing = False

        pygame.event.pump()

        screen.fill(pygame.Color('#0f380f'))

        if playing and not show_menu:
            particles_g.update(screen_rect, dt)
            bullets_g.update(screen_rect, dt)
            enemies_g.update(screen, screen_rect,
                             (player.rect.x, player.rect.y),
                             dt)
            enemy_spawn.update(dt)
            items_g.update(dt)
            enemy_bullet_g.update(screen_rect, dt)
            player_g.update(screen, screen_rect, dt)

        bullets_g.draw(screen)
        enemy_bullet_g.draw(screen)
        particles_g.draw(screen)
        enemies_g.draw(screen)
        items_g.draw(screen)
        player_g.draw(screen)

        render_hitbox(screen, player, enemies_g,
                      bullets_g, enemy_bullet_g, items_g,
                      show_rect, show_hitbox)

        score_label.update(player.score)

        health.update(player.health)

        active_effects = []

        if player.shield and shield_bar not in active_effects:
            active_effects.append(shield_bar)
        if player.speed_boost and speed_boost_bar not in active_effects:
            active_effects.append(speed_boost_bar)
        if player.magnet and magnet_bar not in active_effects:
            active_effects.append(magnet_bar)

        if not player.shield and shield_bar in active_effects:
            active_effects.remove(shield_bar)
        if not player.speed_boost and speed_boost_bar in active_effects:
            active_effects.remove(speed_boost_bar)
        if not player.magnet and magnet_bar in active_effects:
            active_effects.remove(magnet_bar)

        for index, effect_bar in enumerate(active_effects):
            effect_bar.pos = (10, 90 + index * 40)
            if effect_bar == speed_boost_bar:
                effect_bar.update(player.speed_boost_timer,
                                  False)
            elif effect_bar == shield_bar:
                effect_bar.update(player.shield_timer,
                                  False)
            elif effect_bar == magnet_bar:
                effect_bar.update(player.magnet_timer,
                                  False)

        ammo_msg = player.ammo
        ammo.max = player.blaster['Max Ammo'][0]

        ammo.update(ammo_msg)

        fps_label.update(f'FPS: {round(clock.get_fps())}')
        # if show_hint:
        #     hint_label.update('[Q] - quit. [R] - restart (upon death). '
        #                       '[Esc] - pause/unpause. [F2] - toggle hint.')

        if not playing:
            if player.health > 0:
                pause_label.update('Paused')
            else:
                dead_label.update('Defeated')

        if show_menu:
            screen.blit(menu.bg, (0, 0))
            menu.update(screen)

        coin_label.update(player.coins)

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick(FPS)

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
