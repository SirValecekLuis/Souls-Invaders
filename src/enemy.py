"""This file is for Enemy class that is basically any creature in the game except the player itself."""
import random

import pygame

from direction import Direction
from ship import Ship
from sounds import Sounds


class Enemy(Ship):
    """This is a class that represents any enemy in the game and derives from Ship."""

    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 hp: float,
                 damage: float,
                 shooting_speed: float,
                 texture: pygame.Surface,
                 sounds: Sounds,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, hp, damage, shooting_speed, texture, sounds, screen)
        self.direction = random.choice([Direction.LEFT, Direction.RIGHT])
        if self.direction == Direction.LEFT:
            self.speed_x *= -1

    def random_movement(self, enemies):
        """Checks if the enemy should move to the other side or not."""
        for enemy in enemies:
            if enemy is not self and self.rect.colliderect(enemy.rect):
                self.speed_x *= -1
                self.move()
                return

        if not self.move():
            self.speed_x *= -1
            self.move()
            return
