"""This file deals with all events in the game and is reacting to them."""
import pygame

from bullet import Bullets
from direction import Direction
from enemy_handler import EnemyHandler
from ship import Player
from textures import Textures


class Events:
    """This class handles all events in the game such as key pressing and calls corresponding functions."""

    @staticmethod
    def check_game_state(player: Player, bullets: Bullets, enemy_handler: EnemyHandler, textures: Textures) -> bool:
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
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.speed_x *= -1
            player.move()
            player.speed_x *= -1

        if keys[pygame.K_SPACE]:
            if player.can_shoot():
                bullet = player.shoot(textures["screen"].get_size()[1] // 32, enemy_handler.enemies, Direction.UP,
                                      textures["player_bullet"])

                bullets.append(bullet)

        return True
