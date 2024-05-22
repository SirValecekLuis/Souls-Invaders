import pygame
from enum import Enum


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
              direction: Direction,
              texture: pygame.Surface,
              sound_effect: pygame.mixer.Sound) -> None:
        if self.bullet is not None:
            return

        if direction == direction.UP:
            speed *= -1

        self.bullet = Bullet(self.rect.x + self.rect.width / 2 - texture.get_width() / 2,
                             self.rect.y,
                             texture.get_width(),
                             texture.get_height(),
                             0,
                             speed,
                             self.damage,
                             texture,
                             self.screen
                             )
        sound_effect.play()
        self.bullet.draw()

    def check_bullet(self, enemies: list) -> None:
        if self.bullet is None:
            return

        # When bullet hits the edge, it vanishes
        if not self.bullet.move():
            self.bullet = None
            return

        for enemy in enemies:
            if self.bullet.rect.colliderect(enemy.rect):
                enemy.hp -= 10
                self.bullet = None
                return

        # If nothign happened, bullet is shown
        self.bullet.draw()

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

    def random_movement(self):
        if not self.move():
            self.speed_x *= -1

        self.move()


class Bullet(PygameObject):
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 damage: int,
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.damage = damage
