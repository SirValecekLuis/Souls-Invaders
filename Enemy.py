import pygame
from Ship import Ship
import random
from Direction import Direction


class Enemy(Ship):
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
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, hp, damage, shooting_speed, texture, screen)
        self.direction = random.choice([Direction.LEFT, Direction.RIGHT])
        if self.direction == Direction.LEFT:
            self.speed_x *= -1

    def random_movement(self, enemies):
        for enemy in enemies:
            if enemy is not self and self.rect.colliderect(enemy.rect):
                self.speed_x *= -1
                self.move()
                return

        if not self.move():
            self.speed_x *= -1
            self.move()
            return
