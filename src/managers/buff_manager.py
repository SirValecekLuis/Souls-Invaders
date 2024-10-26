"""This file contains all classes and things necessary for buffs to work."""

import random
import pygame.rect

from src.managers.screen_manager import ScreenManager
from src.managers.time_manager import TimeManager
from src.objects.buff import BuffType, Buff
from src.objects.ship import Player
from src.managers.service_manager import ServiceManager
from src.managers.sound_manager import SoundManager
from src.managers.texture_manager import TextureManager


class BuffManager:
    """This class handles all the buffs, shows them, checks them, etc."""

    def __init__(self, player: Player) -> None:
        self.buffs = []
        self.active_buffs = []
        self.player = player
        self.textures = ServiceManager.get(TextureManager)
        self.screen = ServiceManager.get(ScreenManager)
        self.sounds = ServiceManager.get(SoundManager)
        self.time = ServiceManager.get(TimeManager)
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
                return Buff(rect.x, rect.y, rect.width, rect.height, 0, 0, buff_type, texture)

    def spawn_buff(self) -> None:
        """
        If time elapsed, this will spawn a buff randomly on the screen.
        :return: None
        """
        if self.time.get_total_time() - self.last_time_spawned < self.time_wait:
            return

        buff_type = random.choice(list(BuffType))
        texture = self.textures[buff_type.name.lower()]
        buff = self._create_buff(buff_type, texture)
        self.buffs.append(buff)
        sound = self.sounds["buff_spawned"]
        sound.set_volume(0.15)
        sound.play()

        self.last_time_spawned = self.time.get_total_time()

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
