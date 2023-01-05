import sys

import pygame

from src.player import Player
from src.projectile import Projectile
from src.slime import Slime
from src.gui import GUI

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    display = pygame.display.set_mode((1920, 1200))
    clock = pygame.time.Clock()
    player = Player(1920 // 2, 1200 // 2, 42, 52, "Sandro")
    gui = GUI(display, player)

    tree = pygame.image.load("../assets/tree_2.png")
    tree = pygame.transform.scale(tree, (150, 250))

    enemies = [Slime(400, 300, display),
               Slime(700, 500, display),
               Slime(900, 100, display)]
    player_projectiles = []

    display_scroll = [0, 0]

    while True:

        player_projectiles = [p for p in player_projectiles if p.alive]
        enemies = [ e for e in enemies if e.alive]



        display.fill((23, 164, 86))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_projectiles.append(Projectile(x=player.x, y=player.y, y_mouse=mouse_y, x_mouse=mouse_x, size=25, speed=10))
                if event.button == 3:
                    player_projectiles.append(
                        Projectile(x=player.x, y=player.y, y_mouse=mouse_y, x_mouse=mouse_x, color=(0, 0, 255), speed=5,
                                   size=45))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            display_scroll[0] -= 5
            #for p in player_projectiles:
                #p.x += 5
            player.animation_counter += 10
            player.moving_left = True
            player.moving_right = False
        if keys[pygame.K_d]:
            display_scroll[0] += 5
            #for p in player_projectiles:
                #p.x -= 5
            player.animation_counter += 10
            player.moving_right = True
            player.moving_left = False

        if keys[pygame.K_w]:
            display_scroll[1] -= 5
            #for p in player_projectiles:
               # p.x += 5
        if keys[pygame.K_s]:
            display_scroll[1] += 5
            #for p in player_projectiles:
                # p.x -= 5

        for p in player_projectiles:
            p.draw(display, enemies)
        for enemy in enemies:
            enemy.draw(display_scroll, player, player_projectiles)

        player.draw(display)
        display.blit(tree, (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))
        display.blit(tree, (300 - display_scroll[0], 300 - display_scroll[1], 16, 16))
        display.blit(tree, (100 - display_scroll[0], 600 - display_scroll[1], 16, 16))

        gui.draw()

        clock.tick(60)
        pygame.display.update()
