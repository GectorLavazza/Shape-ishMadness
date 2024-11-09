import asyncio
import time

from cursor import Cursor
from enemies import *
from player import Player
from sound import SoundPlayer
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
        "Player": {"Hp": [10, 10, 30, 2, 50],
                   "Crit %": [1, 1, 5, 1, 50],
                   "Spd": [5, 5, 8, 1, 50]},
        "Blaster": {"Dmg": [1, 1, 10, 1, 20],
                    "Cooldown": [30, 30, 5, -5, 5],
                    'Max Ammo': [50, 50, 1000, 50, 10]},
        'Blaster+': {'Range': [60, 60, 240, 10, 10],
                     'Amount': [1, 1, 21, 2, 30],
                     'Angle': [10, 10, 90, 10, 50]},
        "Spd Boost": {"Time": [600, 600, 1200, 100, 40],
                      "Boost": [1, 1, 4, 1, 60]},
        "Shield": {"Time": [600, 600, 1200, 100, 40],
                   "Protection": [1, 1, 9, 1, 60]},
        "Magnet": {"Time": [300, 300, 600, 100, 40],
                   "Force": [5, 5, 15, 2, 60]}
    }

    data = Data(d)

    sound_player = SoundPlayer()

    particles_g = pygame.sprite.Group()
    bullets_g = pygame.sprite.Group()
    enemies_g = pygame.sprite.Group()
    items_g = pygame.sprite.Group()
    enemy_bullet_g = pygame.sprite.Group()
    cursor_g = pygame.sprite.Group()

    player_g = pygame.sprite.Group()
    player = Player(bullets_g, particles_g, enemy_bullet_g, data, sound_player,
                    player_g)

    enemy_spawn = EnemySpawn(enemies_g, particles_g, bullets_g, items_g,
                             enemy_bullet_g, player, sound_player)

    score_label = Text(screen, size, 40, pos=(SW // 2, 25))

    health = ValueBar(screen, size, player.max_health, 'heart', (10, 10))

    ammo = ValueBar(screen, size, 20, 'ammo', (10, 50))

    speed_boost_bar = ValueBar(screen, size, player.max_speed_boost_time,
                               'speed_boost', (10, 0))
    shield_bar = ValueBar(screen, size, player.max_speed_boost_time, 'shield',
                          (10, 0))
    magnet_bar = ValueBar(screen, size, player.max_magnet_time, 'magnet',
                          (10, 0))

    cursor = Cursor(player, cursor_g)

    fps_label = Text(screen, size, 10, pos=(10, SH - 15), center_align=False)
    enemies_label = Text(screen, size, 10, pos=(10, SH - 30),
                         center_align=False)
    items_label = Text(screen, size, 10, pos=(10, SH - 45), center_align=False)
    bullets_label = Text(screen, size, 10, pos=(10, SH - 60),
                         center_align=False)
    particles_label = Text(screen, size, 10, pos=(10, SH - 75),
                           center_align=False)

    f7_label = Text(screen, size, 10, pos=(SW - 10, SH - 15),
                    center_align=False, right_align=True)
    f6_label = Text(screen, size, 10, pos=(SW - 10, SH - 30),
                    center_align=False, right_align=True)
    f5_label = Text(screen, size, 10, pos=(SW - 10, SH - 45),
                    center_align=False, right_align=True)
    f4_label = Text(screen, size, 10, pos=(SW - 10, SH - 60),
                    center_align=False, right_align=True)
    f3_label = Text(screen, size, 10, pos=(SW - 10, SH - 75),
                    center_align=False, right_align=True)
    f2_label = Text(screen, size, 10, pos=(SW - 10, SH - 90),
                    center_align=False, right_align=True)
    r_label = Text(screen, size, 10, pos=(SW - 10, SH - 105),
                   center_align=False, right_align=True)
    esc_label = Text(screen, size, 10, pos=(SW - 10, SH - 120),
                     center_align=False, right_align=True)
    e_label = Text(screen, size, 10, pos=(SW - 10, SH - 135),
                   center_align=False, right_align=True)

    song_label = Text(screen, size, 10, pos=(SW - 10, SH - 165),
                      center_align=False, right_align=True)

    hint_label = Text(screen, size, 12, pos=(SW // 2, SH - 15))

    pause_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))
    dead_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))

    coin_label = CoinsCount(screen, size, 30, 'white', pos=(SW - 50, 10))

    menu = UpgradesMenu(screen, (SW, SH), data, player, sound_player)

    show_hint = True
    show_hitbox = False
    show_rect = False
    show_debug = False

    playing = True
    show_menu = False

    song_index = 0

    max_particles = 0
    max_items = 0
    max_bullets = 0
    max_enemies = 0
    max_fps = 0
    min_fps = 1000

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
                        cursor_g = pygame.sprite.Group()

                        player_g = pygame.sprite.Group()

                        d = {
                            "Player": {"Hp": [10, 10, 30, 2, 50],
                                       "Crit %": [1, 1, 5, 1, 50],
                                       "Spd": [5, 5, 8, 1, 50]},
                            "Blaster": {"Dmg": [1, 1, 10, 1, 20],
                                        "Cooldown": [30, 30, 5, -5, 5],
                                        'Max Ammo': [50, 50, 1000, 50, 10]},
                            'Blaster+': {'Range': [60, 60, 240, 10, 10],
                                         'Amount': [1, 1, 21, 2, 30],
                                         'Angle': [10, 10, 90, 10, 50]},
                            "Spd Boost": {"Time": [600, 600, 1200, 100, 40],
                                          "Boost": [1, 1, 4, 1, 60]},
                            "Shield": {"Time": [600, 600, 1200, 100, 40],
                                       "Protection": [1, 1, 9, 1, 60]},
                            "Magnet": {"Time": [300, 300, 600, 100, 40],
                                       "Force": [5, 5, 15, 2, 60]}
                        }

                        data = Data(d)
                        player = Player(bullets_g, particles_g, enemy_bullet_g,
                                        data, sound_player, player_g)

                        health = ValueBar(screen, size, player.max_health,
                                          'heart', (10, 10))

                        cursor = Cursor(player, cursor_g)

                        menu = UpgradesMenu(screen, (SW, SH), data, player,
                                            sound_player)

                        enemy_spawn = EnemySpawn(enemies_g, particles_g,
                                                 bullets_g,
                                                 items_g, enemy_bullet_g,
                                                 player, sound_player)

                if event.key == pygame.K_ESCAPE:
                    if player.health and not show_menu:
                        playing = not playing

                if event.key == pygame.K_e:
                    if player.health and playing:
                        show_menu = not show_menu

                if event.key == pygame.K_F1:
                    show_hint = not show_hint

                if event.key == pygame.K_F2:
                    show_debug = not show_debug

                if event.key == pygame.K_F3:
                    show_hitbox = not show_hitbox

                if event.key == pygame.K_F4:
                    show_rect = not show_rect

                if event.key == pygame.K_F5:
                    if sound_player.volume:
                        sound_player.volume = 0
                    else:
                        sound_player.volume = 0.5

                if event.key == pygame.K_F6:
                    if sound_player.music_set:
                        song_index += 1
                    if song_index >= len(SONGS):
                        song_index = 0
                    sound_player.set_music(SONGS[song_index])

                if event.key == pygame.K_F7:
                    if sound_player.music_set:
                        if sound_player.music_volume:
                            sound_player.set_music_volume(0)
                        else:
                            sound_player.set_music_volume(0.5)

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

                if event.key == pygame.K_F12:
                    if event.mod & pygame.KMOD_CTRL and event.mod & pygame.KMOD_SHIFT:
                        d = CHEAT_DATA.copy()
                        data.data = d
                        player.update_stats(data, menu)
                        player.cheat(d)
                        health.max = player.max_health
                        shield_bar.max = player.max_shield_time
                        speed_boost_bar.max = player.max_speed_boost_time
                        magnet_bar.max = player.max_magnet_time

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
                            magnet_bar.max = player.max_magnet_time
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

        # if show_hint:
        #     hint_label.update('[E] - upgrades menu. [R] - restart (upon death). '
        #                       '[Esc] - pause/unpause. [F1] - toggle hint.')

        if not playing:
            if player.health > 0:
                pause_label.update('Paused')
            else:
                dead_label.update('Defeated')

        if show_menu:
            screen.blit(menu.bg, (0, 0))
            menu.update(screen)

        coin_label.update(player.coins)

        if show_debug:
            if len(particles_g) > max_particles:
                max_particles = len(particles_g)

            if len(enemies_g) > max_enemies:
                max_enemies = len(enemies_g)

            if len(bullets_g) + len(enemy_bullet_g) > max_bullets:
                max_bullets = len(bullets_g) + len(enemy_bullet_g)

            if len(items_g) > max_items:
                max_items = len(items_g)

            if len(particles_g) > max_particles:
                max_particles = len(particles_g)

            if round(clock.get_fps()) > max_fps:
                max_fps = round(clock.get_fps())

            if round(clock.get_fps()) < min_fps:
                min_fps = round(clock.get_fps())

            fps_label.update(f'FPS: {round(clock.get_fps())} / {min_fps} / {max_fps}')
            enemies_label.update(f'Enemies: {len(enemies_g)} / {max_enemies}')
            items_label.update(f'Items: {len(items_g)} / {max_items}')
            bullets_label.update(
                f'Bullets: {len(bullets_g) + len(enemy_bullet_g)} / {max_bullets}')
            particles_label.update(f'Particles: {len(particles_g)} / {max_particles}')

            e_label.update('[E] - upgrades menu')
            esc_label.update('[Esc] - pause/unpause')
            r_label.update('[R] - restart (upon defeat)')
            f2_label.update('[F2] - toggle debug (this)')
            f3_label.update('[F3] - toggle hitbox')
            f4_label.update('[F4] - toggle rect')
            f5_label.update('[F5] - toggle sfx volume')
            f6_label.update('[F6] - turn/switch music')
            f7_label.update('[F7] - toggle music volume')

            song_label.update(f'Music [{song_index + 1}/{len(SONGS)}]: '
                              f'{SONGS[song_index]}')

        sound_player.update(dt)

        cursor_g.draw(screen)
        cursor.update()

        pygame.display.flip()
        clock.tick(FPS)

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
