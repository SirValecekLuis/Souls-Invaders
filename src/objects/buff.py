from enum import Enum
import pygame

from src.managers.service_manager import ServiceManager
from src.managers.time_manager import TimeManager
from src.objects.pygame_object import PygameObject
from src.objects.ship import Player

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
                 texture: pygame.Surface | None) -> None:
        """
        :param x: x coord
        :param y: y coord
        :param w: width
        :param h: height
        :param speed_x: 0 as buff is not moving
        :param speed_y: 0 as buff is not moving
        :param buff_type: Based on enum BuffType
        :param texture: texture that buff should have
        :return: None
        """

        super().__init__(x, y, w, h, speed_x, speed_y, texture)
        self.buff_type = buff_type
        self.time_when_applied = None
        self.time = ServiceManager.get(TimeManager)
        self.time_spawned = self.time.get_total_time()
        self.time_buff = 5_000
        self.time_expiration = 60_000

    def ended(self) -> bool:
        """
        Returns true if the buff ended and player's stat buff should be removed.
        :return: Bool
        """
        return self.time.get_total_time() - self.time_when_applied > self.time_buff

    def is_expired(self) -> bool:
        """
        Returns true when the buff is too long on the main screen and should be removed to have space for new buffs.
        :return: Bool
        """
        return self.time.get_total_time() - self.time_spawned > self.time_expiration

    def apply_buff(self, player: Player) -> None:
        """
        This function is called when a buff is picked up
        :param player: Player that picked up the buff
        :return: None
        """
        self.time_when_applied = self.time.get_total_time()

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
