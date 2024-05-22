import pygame
from enum import Enum
import random
import gif_pygame
import time


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class PygameObject:
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.texture = texture
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self) -> None:
        self.screen.blit(self.texture, self.rect.topleft)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def move(self) -> bool:
        screen_w, screen_h = pygame.display.get_window_size()

        if self.rect.x + self.rect.width + self.speed_x > screen_w or self.rect.x + self.speed_x < 0:
            return False

        if self.rect.y + self.rect.height + self.speed_y > screen_h or self.rect.y + self.speed_y < 0:
            return False

        self.rect = self.rect.move(self.speed_x, self.speed_y)
        return True


class Ship(PygameObject):
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 hp: int,
                 damage: int,
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.bullet = None
        self.hp = hp
        self.damage = damage

    def shoot(self,
              speed: float,
              enemies: list,
              direction: Direction,
              texture: pygame.Surface,
              sound_effect: pygame.mixer.Sound | None):

        if self.bullet is not None:
            return None

        if direction == direction.UP:
            speed *= -1

        self.bullet = Bullet(self.rect.x + self.rect.width / 2 - texture.get_width() / 2,
                             self.rect.y,
                             texture.get_width(),
                             texture.get_height(),
                             0,
                             speed,
                             self.damage,
                             enemies,
                             self,
                             texture,
                             self.screen
                             )

        if sound_effect:
            sound_effect.play()

        return self.bullet

    def is_alive(self):
        return self.hp > 0


class Enemy(Ship):
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 hp: int,
                 damage: int,
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, hp, damage, texture, screen)
        self.direction = Direction.LEFT

    def random_movement(self, enemies):
        if not self.move():
            self.speed_x *= -1
            self.move()
            return

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.speed_x *= -1
                self.move()
                return


class Bullet(PygameObject):
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 damage: int,
                 enemies: list,
                 ship: Ship,
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.damage = damage
        self.enemies = enemies
        self.ship = ship

    def check_bullet(self) -> bool:
        """
        Checks if the bullet is about to be destroyed or not False if it should be destroyed, True if stays
        :return: bool
        """

        # When bullet hits the edge, it vanishes
        if not self.move():
            self.ship.bullet = None
            return False

        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.hp -= 10
                self.ship.bullet = None
                return False

        # If nothing happened, bullet is shown
        return True


class Effect:
    def __init__(self, duration: float, effect: gif_pygame.GIFPygame, rect: pygame.rect.Rect, screen: pygame.Surface):
        self.effect = effect
        gif_pygame.transform.scale(self.effect, (rect.width, rect.height))
        self.rect = rect
        self.screen = screen
        self.duration = duration
        self.start_time = time.time()

    def update(self) -> bool:
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= self.duration:
            return False

        self.effect.render(self.screen, self.rect)

        return True
