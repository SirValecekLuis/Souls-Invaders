import pygame
from PygameObject import PygameObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ship import Ship


class Bullet(PygameObject):

    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 enemies: list,
                 ship: 'Ship',
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.enemies = enemies
        self.ship = ship

    def check_bullet(self) -> bool:
        """
        Checks if the bullet is about to be destroyed or not False if it should be destroyed, True if stays
        :return: bool
        """

        # When bullet hits the edge, it vanishes
        if not self.move():
            self.ship.last_time_shot = 0
            return False

        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.hp -= self.ship.damage
                self.ship.last_time_shot = 0
                return False

        # If nothing happened, bullet is shown
        return True


class Bullets:
    def __init__(self):
        self.bullets = []

    def update_all_bullets(self) -> None:
        for i in range(len(self.bullets) - 1, -1, -1):
            bullet = self.bullets[i]
            if not bullet.check_bullet():
                self.bullets.pop(i)
                continue
            bullet.draw()

    def append(self, bullet: Bullet):
        self.bullets.append(bullet)
