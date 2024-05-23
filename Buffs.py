import random
from enum import Enum

import pygame.rect

from PygameObject import PygameObject
from Ship import Player
from Sounds import Sounds
from Textures import Textures


class BuffType(Enum):
    DAMAGE = 1
    HEAL = 2
    SPEED = 3


class Buff(PygameObject):
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 buff_type: BuffType,
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.buff_type = buff_type
        self.time_when_applied = None
        self.time_spawned = pygame.time.get_ticks()
        self.time_buff = 5_000
        self.time_expiration = 60_000

    def ended(self) -> bool:
        return pygame.time.get_ticks() - self.time_when_applied > self.time_buff

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.time_spawned > self.time_expiration

    def apply_buff(self, player: Player):
        self.time_when_applied = pygame.time.get_ticks()

        if self.buff_type == BuffType.HEAL:
            player.heal(10)
        elif self.buff_type == BuffType.DAMAGE:
            player.damage *= 2
        elif self.buff_type == BuffType.SPEED:
            player.speed_x *= 1.5

    def deactivate_buff(self, player: Player):
        if self.buff_type == BuffType.DAMAGE:
            player.damage /= 2
        elif self.buff_type == BuffType.SPEED:
            player.speed_x /= 1.5


class Buffs:
    def __init__(self, player: Player, textures: Textures, sounds: Sounds, screen: pygame.Surface):
        self.buffs = []
        self.active_buffs = []
        self.player = player
        self.textures = textures
        self.screen = screen
        self.sounds = sounds
        self.last_time_spawned = -5_000
        self.time_wait = 15_000

    def _create_buff(self, buff_type: BuffType, texture: pygame.Surface) -> Buff:
        while True:
            rect = pygame.Rect(random.randrange(0, self.screen.get_width() - texture.get_width()),
                               self.screen.get_height() - self.player.rect.height / 2 - texture.get_height() / 2,
                               texture.get_width(),
                               texture.get_height())

            if rect.colliderect(self.player.rect):
                continue

            for buff in self.buffs:
                if rect.colliderect(buff.rect):
                    break
            else:
                return Buff(rect.x, rect.y, rect.width, rect.height, 0, 0, buff_type, texture, self.screen)

    def spawn_buff(self) -> None:
        if pygame.time.get_ticks() - self.last_time_spawned < self.time_wait:
            return

        buff_type = random.choice(list(BuffType))
        texture = self.textures[buff_type.name.lower()]
        buff = self._create_buff(buff_type, texture)
        self.buffs.append(buff)
        sound = self.sounds["buff_spawned"]
        sound.set_volume(0.15)
        sound.play()

        self.last_time_spawned = pygame.time.get_ticks()

    def check_all_buffs(self):
        # Check spawned buffs
        for i in range(len(self.buffs) - 1, -1, -1):
            buff = self.buffs[i]
            if self.player.rect.colliderect(buff.rect):
                self.sounds["bonus_taken"].play()
                buff.apply_buff(self.player)
                self.active_buffs.append(buff)
                self.buffs.pop(i)
                continue

            if buff.is_expired():
                self.buffs.pop(i)

        # Check applied buffs
        for i in range(len(self.active_buffs) - 1, - 1, -1):
            buff = self.active_buffs[i]
            if buff.ended():
                buff.deactivate_buff(self.player)
                self.active_buffs.pop(i)

    def draw_all_buffs(self):
        for buff in self.buffs:
            buff.draw()
