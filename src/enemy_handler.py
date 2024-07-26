"""This file is for enemy handler that deals with waves, enemies and overall sets the game and how it proceeds."""
import random

import pygame

from bullet import Bullets
from direction import Direction
from effects import Effects
from enemy import Enemy
from game_screen import GameScreen
from ship import Player
from sounds import Sounds
from textures import Textures


class EnemyHandler:
    """This class handles all the enemies and will deal with waves in the game and spawning."""

    def __init__(self, sounds: Sounds, textures: Textures, effects: Effects):
        self.phase = 1
        self.enemies = []
        self.time_pause = None
        self.time_wait = 0  # ms
        self.sounds = sounds
        self.textures = textures
        self.effects = effects

    def generate_enemy(self,
                       speed_x: float,
                       hp: float,
                       damage: float,
                       shooting_speed: float,
                       count: int,
                       boss: bool,
                       enemy_texture: pygame.Surface | None,
                       screen: pygame.Surface) -> None:
        """
        This function ensures that there are only enemies between count 0 to 50 and spawns an enemy
        :param speed_x: Speed of enemy
        :param hp: Hp of enemy
        :param damage: Damage dealt by enemy
        :param shooting_speed: Shooting speed
        :param count: Enemies count
        :param boss: True or False
        :param enemy_texture: Texture
        :param screen: Pygame screen
        :return: None
        """
        if count > 50 or count < 0:
            raise Exception("Invalid amount of enemies to spawn")

        # For bosses
        if boss:
            enemy = Enemy(
                random.randrange(enemy_texture.get_width(), screen.get_width() - enemy_texture.get_width()),
                random.randrange(screen.get_height() // 10,
                                 screen.get_height() // 2 - enemy_texture.get_height()),
                enemy_texture.get_width(),
                enemy_texture.get_height(),
                speed_x,
                0,
                hp,
                damage,
                shooting_speed,
                enemy_texture,
                self.sounds,
                screen)
            self.enemies.append(enemy)
            return

        y_list = [i * enemy_texture.get_height() for i in
                  range(int(screen.get_height() // 2.5 // enemy_texture.get_height()))]
        i = 0
        collision = False
        while i < count:
            x = random.randrange(enemy_texture.get_width(), screen.get_width() - enemy_texture.get_width())
            y = random.choice(y_list)
            new_enemy = Enemy(x,
                              y,
                              enemy_texture.get_width(),
                              enemy_texture.get_height(),
                              speed_x,
                              0,
                              hp,
                              damage,
                              shooting_speed,
                              enemy_texture,
                              self.sounds,
                              screen)

            for enemy in self.enemies:
                if new_enemy.rect.colliderect(enemy.rect):
                    collision = True
                    break

            if collision:
                collision = False
                continue

            self.enemies.append(new_enemy)
            i += 1

    def check_phase(self, start_time: int) -> None:
        """
        This function checks in which phase the game is, this will probably be rewritten or removed in the future.
        :param start_time: Start time for the end screen to tell how many minutes the games was running
        :return: None
        """

        if len(self.enemies) != 0:
            return

        # time pause between rounds
        if self.time_pause is None:
            self.time_pause = pygame.time.get_ticks()
            pygame.mixer.music.stop()
            if self.phase != 1:
                self.sounds["laugh"].play()
            return

        if pygame.time.get_ticks() - self.time_pause > self.time_wait:
            self.time_pause = None
        else:
            return

        match self.phase:
            case 1:
                self.generate_enemy(10, 20, 3, 2, 20, False, self.textures["enemy"], self.textures["screen"])
                pygame.mixer.music.load("./sounds/background.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.time_wait = 2000
            case 2:
                self.generate_enemy(15, 1000, 15, 0.45, 1, True, self.textures["boss_1"], self.textures["screen"])
                pygame.mixer.music.load("./sounds/first_boss.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            case 3:
                self.generate_enemy(10, 25, 4, 1.5, 25, False, self.textures["enemy"], self.textures["screen"])
                pygame.mixer.music.load("./sounds/background.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            case 4:
                self.generate_enemy(18, 2000, 30, 0.25, 1, True, self.textures["boss_2"], self.textures["screen"])
                pygame.mixer.music.load("./sounds/second_boss.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.time_wait = 2000
            case _:
                if len(self.enemies) == 0:
                    pygame.mixer.music.stop()
                    self.sounds["game_completed"].play()
                    GameScreen.game_completed_screen(start_time, self.textures["screen"])

        self.phase += 1

    def check_enemies(self, player: Player, bullets: Bullets) -> None:
        """
        This checks all the enemies and plays sounds if enemy dies, etc.
        :param player: Player
        :param bullets: All the bullets in the game
        :return: None
        """

        for i in range(len(self.enemies) - 1, -1, -1):
            enemy = self.enemies[i]
            if not enemy.is_alive():
                self.effects.append(1, self.textures["boom_effect"], enemy.rect, self.textures["screen"])  # Explosion
                self.sounds["small_explosion"].play()  # Sound effect of explosion
                self.enemies.pop(i)
            else:
                enemy.random_movement(self.enemies)
                if enemy.can_shoot():
                    bullet = enemy.shoot(self.textures["screen"].get_size()[1] // 64, [player], Direction.DOWN,
                                         self.textures["enemy_bullet"])

                    bullets.append(bullet)
                i += 1

    def draw_all_enemies(self):
        """Goes through all enemies and draws them."""
        for enemy in self.enemies:
            enemy.draw()
