"""This file handles all classes that are somehow connected to bullets, and any other projectiles shot in the game."""
from typing import TYPE_CHECKING

import pygame

from pygame_object import PygameObject
from sounds import Sounds

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
                 texture: pygame.Surface | None,
                 sounds: Sounds,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.sounds = sounds
        self.enemies = enemies
        self.ship = ship

    def check_bullet(self) -> bool:
        """
        Checks if the bullet is about to be destroyed or not False if it should be destroyed, True if stays
        :return: Bool
        """
        from ship import Player  # pylint: disable=import-outside-toplevel

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


class Bullets:
    """This class handles all projectiles that derive from class Bullet and will check collision and draws them."""

    def __init__(self):
        self.bullets = []

    def check_bullets(self) -> None:
        """Checks all the bullets and things that derive from Bullet class on the screen."""
        for i in range(len(self.bullets) - 1, -1, -1):
            bullet = self.bullets[i]
            if not bullet.check_bullet():
                self.bullets.pop(i)
                continue

    def draw_all_bullets(self):
        """Called every frame to draw all bullets on the screen and move them."""
        for bullet in self.bullets:
            bullet.draw()

    def append(self, bullet: Bullet):
        """Adds a Bullet class instance in the list to check on it next frame."""
        self.bullets.append(bullet)
