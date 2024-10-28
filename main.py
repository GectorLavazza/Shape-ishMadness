import pygame
import time
import asyncio

from particles import *

from enemies import *
from player import Player

from settings import *
from ui import *


async def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    screen, size, screen_rect = set_screen((SW, SH))

    last_time = time.time()

    running = True

    particles_g = pygame.sprite.Group()
    bullets_g = pygame.sprite.Group()
    enemies_g = pygame.sprite.Group()
    items_g = pygame.sprite.Group()
    enemy_bullet_g = pygame.sprite.Group()
    buttons_g = pygame.sprite.Group()

    player_button = Button(load_image('player_button'), (0, 0), buttons_g)

    player_g = pygame.sprite.Group()
    player = Player(bullets_g, particles_g, enemy_bullet_g, player_g)

    enemy_spawn = EnemySpawn(enemies_g, particles_g, bullets_g, items_g,
                             enemy_bullet_g, player)

    score_label = Text(screen, size, 40, pos=(SW // 2, 25))

    health = ValueBar(screen, size, player.max_health, 'heart', (10, 10))

    ammo = ValueBar(screen, size, 20, 'ammo', (10, 50))

    speed_boost_bar = ValueBar(screen, size, player.max_speed_boost_time, 'speed_boost', (10, 0))
    shield_bar = ValueBar(screen, size, player.max_speed_boost_time, 'shield', (10, 0))


    fps_label = Text(screen, size, 10, pos=(40, SH - 15))

    hint_label = Text(screen, size, 12, pos=(SW // 2, SH - 15))

    pause_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))
    dead_label = Text(screen, size, 60, pos=(SW // 2, SH // 2))

    coin_label = CoinsCount(screen, size, 30, 'white', pos=(SW - 50, 10))

    menu = Menu(screen, (SW, SH), buttons_g, (SW // 2, SH // 2))

    # play_music(SONGS[0], 0.3)

    show_hint = True
    show_hitbox = False
    show_rect = False

    playing = True
    show_menu = False

    mouse_wheel_cd = 0

    while running:

        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        mouse_wheel_cd += dt

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                if mouse_wheel_cd >= 10:
                    player.cooldown = 0
                    mouse_wheel_cd = 0
                    if event.y == -1:
                        if 0 <= player.mode - event.y <= 2:
                            player.mode -= event.y
                        else:
                            player.mode = 0
                    else:
                        if 2 >= player.mode - event.y >= 0:
                            player.mode -= event.y
                        else:
                            player.mode = 2

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if not playing:
                        running = False

                if event.key == pygame.K_r:
                    if player.health <= 0:
                        playing = True

                        particles_g = pygame.sprite.Group()
                        bullets_g = pygame.sprite.Group()
                        enemies_g = pygame.sprite.Group()
                        items_g = pygame.sprite.Group()
                        enemy_bullet_g = pygame.sprite.Group()

                        player_g = pygame.sprite.Group()
                        player = Player(bullets_g, particles_g, enemy_bullet_g,
                                        player_g)

                        enemy_spawn = EnemySpawn(enemies_g, particles_g, bullets_g,
                                                 items_g, enemy_bullet_g, player)

                if event.key == pygame.K_ESCAPE:
                    if player.health and not show_menu:
                        playing = not playing

                if event.key == pygame.K_e:
                    if player.health and playing:
                        show_menu = not show_menu

                if event.key == pygame.K_F1:
                    if fps == 120:
                        fps = 60
                    elif fps == 60:
                        fps = 10
                    elif fps == 10:
                        fps = 120

                if event.key == pygame.K_F2:
                    show_hint = not show_hint

                if event.key == pygame.K_F3:
                    show_hitbox = not show_hitbox

                if event.key == pygame.K_F4:
                    show_rect = not show_rect

                if event.key == pygame.K_LSHIFT:
                    player.sprint = True

                if event.key == pygame.K_w:
                    player.dy = -1
                if event.key == pygame.K_s:
                    player.dy = 1
                if event.key == pygame.K_a:
                    player.dx = -1
                if event.key == pygame.K_d:
                    player.dx = 1

                if event.key == pygame.K_1:
                    player.mode = 0
                    player.cooldown = 0
                if event.key == pygame.K_2:
                    player.mode = 1
                    player.cooldown = 0
                if event.key == pygame.K_3:
                    player.mode = 2
                    player.cooldown = 0

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

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    player.hold = False

        if playing and not show_menu:
            if player.hold:
                player.shoot(mouse_pos)

        if player.health <= 0:
            playing = False

        screen.fill(pygame.Color('#0f380f'))

        if playing and not show_menu:
            particles_g.update(screen_rect, dt, fps)
            bullets_g.update(screen_rect, dt)
            enemies_g.update(screen, screen_rect, (player.rect.x, player.rect.y),
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

        if not player.shield and shield_bar in active_effects:
            active_effects.remove(shield_bar)
        if not player.speed_boost and speed_boost_bar in active_effects:
            active_effects.remove(speed_boost_bar)

        for index, effect_bar in enumerate(active_effects):
            effect_bar.pos = (10, 90 + index * 40)
            if effect_bar == speed_boost_bar:
                effect_bar.update(player.speed_boost_timer,
                                  False)
            elif effect_bar == shield_bar:
                effect_bar.update(player.shield_timer,
                                  False)

        ammo_msg = player.weapons[player.mode]['ammo']
        ammo.max = player.weapons[player.mode]['max_ammo']
        ammo.image = load_image(['ammo', 'shotgun_ammo', 'riffle_ammo'][player.mode])

        ammo.update(ammo_msg)

        fps_label.update(f'FPS: {round(clock.get_fps())}')
        if show_hint:
            hint_label.update('[Q] - quit. [R] - restart (upon death). '
                              '[Esc] - pause/unpause. [F2] - toggle hint.')

        if not playing:
            if player.health > 0:
                pause_label.update('Paused')
            else:
                dead_label.update('Defeated')

        if show_menu:
            menu.update()
            buttons_g.draw(screen)

        coin_label.update(player.coins)

        pygame.display.flip()
        clock.tick(fps)

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
