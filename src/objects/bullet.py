"""This file handles all classes that are somehow connected to bullets, and any other projectiles shot in the game."""
from typing import TYPE_CHECKING

import pygame

from src.objects.pygame_object import PygameObject
from src.managers.service_manager import ServiceManager
from src.managers.sound_manager import SoundManager

if TYPE_CHECKING:
    from ship import Ship


class Bullet(PygameObject):
    """This is a basic class for a bullet and be derived from."""

    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 enemies: list,
                 ship: 'Ship',
                 texture: pygame.Surface | None):
        super().__init__(x, y, w, h, speed_x, speed_y, texture)
        self.sounds = ServiceManager.get(SoundManager)
        self.enemies = enemies
        self.ship = ship

    def check_bullet(self) -> bool:
        """
        Checks if the bullet is about to be destroyed or not False if it should be destroyed, True if stays
        :return: Bool
        """
        from src.objects.ship import Player  # pylint: disable=import-outside-toplevel

        # When a bullet hits the edge, it vanishes and resets shoot timer for ship, so it can shoot again
        if not self.move():
            self.ship.reset_shoot_timer()
            return False

        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.hp -= self.ship.damage
                if isinstance(enemy, Player):
                    self.sounds["player_hit"].play()
                self.ship.reset_shoot_timer()
                return False

        # If nothing happened, a bullet is shown
        return True
