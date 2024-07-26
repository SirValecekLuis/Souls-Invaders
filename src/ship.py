"""This file handles basic class Ship which can be inherited."""
from typing import TYPE_CHECKING

import pygame

from direction import Direction
from pygame_object import PygameObject
from sounds import Sounds

if TYPE_CHECKING:
    from bullet import Bullet


class Ship(PygameObject):
    """This class is used for moving entities on screen can be used for inheritance (for an enemy, e.g.)"""

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
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.hp = hp
        self.damage = damage
        self.shooting_speed = shooting_speed * 1000
        self.last_time_shot = pygame.time.get_ticks() - 1800  # Starting delay before shooting
        self.sounds = sounds

    def shoot(self,
              speed: float,
              enemies: list,
              direction: Direction,
              texture: pygame.Surface | None,
              ) -> 'Bullet':
        """
        Shoots a bullet if the player can shoot.
        :param speed: Speed of bullet
        :param enemies: Enemies to check collision against
        :param direction: Bullet direction
        :param texture: Bullet texture
        :return:
        """
        from bullet import Bullet  # pylint: disable=import-outside-toplevel

        if direction == direction.UP:
            speed *= -1

        bullet = Bullet(self.rect.x + self.rect.width / 2 - texture.get_width() / 2,
                        self.rect.y,
                        texture.get_width(),
                        texture.get_height(),
                        0,
                        speed,
                        enemies,
                        self,
                        texture,
                        self.sounds,
                        self.screen
                        )

        if isinstance(self, Player):
            self.sounds["shot_sound"].play()

        self.last_time_shot = pygame.time.get_ticks()
        return bullet

    def can_shoot(self) -> bool:
        """If time elapsed from the last shoot is greater than shooting speed,
        then player can shoot and True is returned."""
        return pygame.time.get_ticks() - self.last_time_shot >= self.shooting_speed

    def is_alive(self) -> bool:
        """Returns True if HP is > 0"""
        return self.hp > 0

    def heal(self, amount: float) -> None:
        """
        Heals player by some amount of HP.
        :param amount: Amount of HP to heal
        :return: None
        """
        self.hp += amount

    def reset_shoot_timer(self):
        """This function will reset the timer when the player last shot, so it makes the player able to shoot again."""
        self.last_time_shot = 0


class Player(Ship):
    """This is a class that derives from Ship and represents a main player."""
    # def __init__(self,
    #              x: float,
    #              y: float,
    #              w: float,
    #              h: float,
    #              speed_x: float,
    #              speed_y: float,
    #              hp: float,
    #              damage: float,
    #              shooting_speed: float,
    #              texture: pygame.Surface,
    #              sounds: Sounds,
    #              screen: pygame.Surface):
    #     super().__init__(x, y, w, h, speed_x, speed_y, hp, damage, shooting_speed, texture, sounds, screen)
