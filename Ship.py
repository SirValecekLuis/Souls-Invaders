from PygameObject import PygameObject
import pygame
from Direction import Direction
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
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.hp = hp
        self.damage = damage
        self.shooting_speed = shooting_speed * 1000
        self.last_time_shot = 0

    def shoot(self,
              speed: float,
              enemies: list,
              direction: Direction,
              texture: pygame.Surface,
              sound_effect: pygame.mixer.Sound | None):

        if pygame.time.get_ticks() - self.last_time_shot < self.shooting_speed:
            return None

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
                        self.screen
                        )

        if sound_effect:
            sound_effect.play()

        self.last_time_shot = pygame.time.get_ticks()
        return bullet

    def is_alive(self):
        return self.hp > 0
