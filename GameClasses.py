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


class Bullet(PygameObject):
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 enemies: list,
                 ship: Ship,
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


class Textures:
    def __init__(self, screen):
        self.textures = dict()
        self.screen = screen
        self.textures["screen"] = screen
        self.load_textures()

    def __getitem__(self, index: str) -> pygame.Surface | gif_pygame.GIFPygame:
        return self.textures[index]

    def load_textures(self):
        self.add_texture("background", self.screen.get_width(), self.screen.get_height())
        self.add_texture("player", 100, 100)
        self.add_texture("enemy", 50, 50)
        self.add_texture("boss_1", 250, 250)
        self.add_texture("boss_2", 250, 250)
        self.add_texture("player_bullet", 40, 40)
        self.add_texture("enemy_bullet", 40, 40)

        self.add_gif("boom_effect")

    def add_texture(self, name: str, size_x=None, size_y=None):
        image = pygame.image.load(f"textures/{name}.png")
        if size_x is not None and size_y is not None:
            image = pygame.transform.scale(image, (size_x, size_y))
        self.textures[name] = image

    def add_gif(self, name: str):
        gif = gif_pygame.load(f"textures/{name}.gif")
        self.textures[name] = gif


class Sounds:
    def __init__(self):
        self.sounds = dict()
        self.load_sounds()

    def __getitem__(self, index: str) -> pygame.mixer.Sound:
        return self.sounds[index]

    def load_sounds(self):
        self.load_wav("shot_sound", 0.3)
        self.load_wav("small_explosion", 0.3)

    def load_wav(self, name: str, volume=0.5):
        self.sounds[name] = pygame.mixer.Sound(f"sounds/{name}.wav")
        self.set_volume(name, volume)

    def load_mp3(self, name: str, volume=0.5):
        self.sounds[name] = pygame.mixer.Sound(f"sounds/{name}.mp3")
        self.set_volume(name, volume)

    def set_volume(self, name: str, volume: float):
        self.sounds[name].set_volume(volume)
