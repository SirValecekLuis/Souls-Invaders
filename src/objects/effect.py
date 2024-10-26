"""This file handles all things that are connected with effect drawing, e.g., boom effect after ship is destroyed."""

import time

import gif_pygame
import pygame

from src.managers.screen_manager import ScreenManager
from src.managers.service_manager import ServiceManager


class Effect:
    """This class represents an effect that can appear on the screen after killing an enemy, e.g."""

    def __init__(self, duration: float, effect: gif_pygame.GIFPygame, rect: pygame.Rect):
        self.effect = effect
        gif_pygame.transform.scale(self.effect, (rect.width, rect.height))
        self.rect = rect
        self.screen = ServiceManager.get(ScreenManager)
        self.duration = duration
        self.start_time = time.time()

    def update(self) -> bool:
        """
        If time elapsed, the function will return False to indicate the effect should be removed and not drawn anymore.
        :return: Bool
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= self.duration:
            return False

        self.effect.render(self.screen.get_screen(), self.rect)

        return True
