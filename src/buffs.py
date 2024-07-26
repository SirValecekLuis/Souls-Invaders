"""This file contains all classes and things necessary for buffs to work."""

import random
from enum import Enum

import pygame.rect

from pygame_object import PygameObject
from ship import Player
from sounds import Sounds
from textures import Textures


class BuffType(Enum):
    """This is enum for buff types, can be expanded in the future with various buffs."""
    DAMAGE = 1
    HEAL = 2
    SPEED = 3


class Buff(PygameObject):
    """This class represents a buff that will appear on the screen each x secs randomly."""

    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 buff_type: BuffType,
                 texture: pygame.Surface | None,
                 screen: pygame.Surface) -> None:
        """
        :param x: x coord
        :param y: y coord
        :param w: width
        :param h: height
        :param speed_x: 0 as buff is not moving
        :param speed_y: 0 as buff is not moving
        :param buff_type: Based on enum BuffType
        :param texture: texture that buff should have
        :param screen: pygame main screen
        :return: None
        """

        super().__init__(x, y, w, h, speed_x, speed_y, texture, screen)
        self.buff_type = buff_type
        self.time_when_applied = None
        self.time_spawned = pygame.time.get_ticks()
        self.time_buff = 5_000
        self.time_expiration = 60_000

    def ended(self) -> bool:
        """
        Returns true if the buff ended and player's stat buff should be removed.
        :return: Bool
        """
        return pygame.time.get_ticks() - self.time_when_applied > self.time_buff

    def is_expired(self) -> bool:
        """
        Returns true when the buff is too long on the main screen and should be removed to have space for new buffs.
        :return: Bool
        """
        return pygame.time.get_ticks() - self.time_spawned > self.time_expiration

    def apply_buff(self, player: Player) -> None:
        """
        This function is called when a buff is picked up
        :param player: Player that picked up the buff
        :return: None
        """
        self.time_when_applied = pygame.time.get_ticks()

        if self.buff_type == BuffType.HEAL:
            player.heal(10)
        elif self.buff_type == BuffType.DAMAGE:
            player.damage *= 2
        elif self.buff_type == BuffType.SPEED:
            player.speed_x *= 1.5

    def deactivate_buff(self, player: Player) -> None:
        """
        This function is called when a buff expired and the player's buff should be removed.
        :param player: Player
        :return: None
        """
        if self.buff_type == BuffType.DAMAGE:
            player.damage /= 2
        elif self.buff_type == BuffType.SPEED:
            player.speed_x /= 1.5


class Buffs:
    """This class handles all the buffs, shows them, checks them, etc."""

    def __init__(self, player: Player, textures: Textures, sounds: Sounds, screen: pygame.Surface) -> None:
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
        """
        If time elapsed, this will spawn a buff randomly on the screen.
        :return: None
        """
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

    def check_all_buffs(self) -> None:
        """
        Goes through all the buffs and decide if buff should disappear as it expired or if buff should be applied to a
        player as it was picked up.
        :return: None"""

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
        """Goes through all the buffs on the screen and calls .draw() on them as they derive from PygameObject."""
        for buff in self.buffs:
            buff.draw()
