from typing import TYPE_CHECKING

import pygame

from Bullet import Bullet
from Direction import Direction
from PygameObject import PygameObject
from Sounds import Sounds

if TYPE_CHECKING:
    from Bullet import Bullet


class Ship(PygameObject):
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
              texture: pygame.Surface,
              ) -> Bullet:

        from Bullet import Bullet

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

    def can_shoot(self):
        return pygame.time.get_ticks() - self.last_time_shot >= self.shooting_speed

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount: float):
        self.hp += amount


class Player(Ship):
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
