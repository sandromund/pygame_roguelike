import pygame
import sys
import random

from src.world import World
from src.assets import Assets
from src.player import Player
from src.gui import GUI
from src.projectile import Projectile
from src.tree import Tree
from src.enemy import Enemy


class Game:

    def __init__(self, wight=1920, height=1200, player_name="Sandro", fps=60):
        pygame.font.init()
        pygame.mixer.init()
        self.assets = Assets()
        pygame.init()
        self.word = World()
        self.wight = wight
        self.height = height
        self.n_enemies = 3
        self.max_enemies = 25
        self.display = pygame.display.set_mode((wight, height))
        self.clock = pygame.time.Clock()
        self.center_x = self.wight // 2
        self.center_y = self.height // 2
        self.player = Player(self.center_x, self.center_y, player_name, self.assets.player_images, self.display)
        self.gui = GUI(self.display, self.player, center=[self.center_x, self.center_y])
        self.background_color = (23, 164, 86)
        self.fps = fps
        self.init_spawn()

    def init_spawn(self):
        self.word.players.append(self.player)
        self.word.trees.append(Tree(display=self.display, x=100, y=100, image=self.assets.tree))
        for _ in range(self.n_enemies):
            self.word.enemies.append(
                Enemy(x=random.randint(0, self.wight), y=random.randint(0, self.height), display=self.display,
                      enemy_images=self.assets.slime_images))

    def main_loop(self):
        self.assets.background_music.play(loops=-1)
        self.assets.background_music.set_volume(0.7)
        while True:
            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.display.fill(self.background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        self.assets.peng_sound.play()
                        self.word.projectiles.append(
                            Projectile(y_mouse=mouse_y, x_mouse=mouse_x, player=self.player, size=25, speed=10))
            self.player.move(keys)
            self.word.draw(self.player.display_scroll_x, self.player.display_scroll_y)
            self.gui.draw()
            self.clock.tick(self.fps)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.main_loop()