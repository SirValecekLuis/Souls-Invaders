"""This file deals with all events in the game and is reacting to them."""
import pygame
from pygame.constants import QUIT, KEYDOWN, KEYUP  # pylint: disable=no-name-in-module

from src.managers.screen_manager import ScreenManager
from src.managers.service_manager import ServiceManager
from src.managers.time_manager import TimeManager
from src.menu.esc_menu import EscMenu
from src.managers.bullet_manager import BulletManager
from src.managers.enemy_manager import EnemyManager
from src.managers.texture_manager import TextureManager
from src.objects.direction import Direction
from src.objects.ship import Player


class EventManager:
    """This class handles all events in the game such as key pressing and calls corresponding functions."""

    def __init__(self, player: Player):
        self.screen = ServiceManager.get(ScreenManager)
        self.bullets = ServiceManager.get(BulletManager)
        self.textures = ServiceManager.get(TextureManager)
        self.enemy_handler = ServiceManager.get(EnemyManager)
        self.time = ServiceManager.get(TimeManager)
        self.player = player
        self.last_time_opened = self.time.get_total_time()

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    def check_game_state(self) -> bool:
        """
        This is called every frame to check what should happen in the game.
        :return: True if everything is correct and game shall continue.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and self.time.get_total_time() - self.last_time_opened > 200:
            esc_menu = EscMenu()
            esc_menu.start()
            self.last_time_opened = self.time.get_total_time()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.speed_x *= -1
            self.player.move()
            self.player.speed_x *= -1

        if keys[pygame.K_SPACE]:
            if self.player.can_shoot():
                bullet = self.player.shoot(self.screen.get_height() // 32, self.enemy_handler.enemies,
                                           Direction.UP,
                                           self.textures["player_bullet"])

                self.bullets.append(bullet)

        return True
