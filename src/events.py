"""This file deals with all events in the game and is reacting to them."""
import pygame

from direction import Direction
from esc_menu import EscMenu
from bullet import Bullets
from enemy_handler import EnemyHandler
from ship import Player
from textures import Textures


class Events:
    """This class handles all events in the game such as key pressing and calls corresponding functions."""

    def __init__(self, screen: pygame.display, bullets: Bullets, textures: Textures, enemy_handler: EnemyHandler,
                 clock: pygame.time.Clock, player: Player):
        self.screen = screen
        self.bullets = bullets
        self.textures = textures
        self.enemy_handler = enemy_handler
        self.clock = clock
        self.player = player

    def check_game_state(self) -> bool:
        """
        This is called every frame to check what should happen in the game.
        :param player: Player
        :param bullets: All bullets
        :param enemy_handler: EnemyHandler class
        :param textures: All Textures
        :return: True if everything is correct and game shall continue.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            esc_menu = EscMenu(self.screen, self.clock)
            esc_menu.start()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.speed_x *= -1
            self.player.move()
            self.player.speed_x *= -1

        if keys[pygame.K_SPACE]:
            if self.player.can_shoot():
                bullet = self.player.shoot(self.textures["screen"].get_size()[1] // 32, self.enemy_handler.enemies,
                                           Direction.UP,
                                           self.textures["player_bullet"])

                self.bullets.append(bullet)

        return True
