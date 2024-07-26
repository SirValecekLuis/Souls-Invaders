"""This file handles all things that are connected with effect drawing, e.g., boom effect after ship is destroyed."""

import time

import gif_pygame
import pygame


class Effect:
    """This class represents an effect that can appear on the screen after killing an enemy, e.g."""

    def __init__(self, duration: float, effect: gif_pygame.GIFPygame, rect: pygame.Rect, screen: pygame.Surface):
        self.effect = effect
        gif_pygame.transform.scale(self.effect, (rect.width, rect.height))
        self.rect = rect
        self.screen = screen
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

        self.effect.render(self.screen, self.rect)

        return True


class Effects:
    """Class that handles all effects in the game (gifs)"""

    def __init__(self):
        self.effects = []

    def update_all_effects(self) -> None:
        """This function checks all the effects and """
        for i in range(len(self.effects) - 1, -1, -1):
            effect = self.effects[i]
            if not effect.update():
                self.effects.pop(i)

    def append(self, duration: float, effect: gif_pygame.GIFPygame, rect: pygame.Rect, screen: pygame.Surface):
        """If effect is created, then is added in the list, so it can be handled by effects class."""
        self.effects.append(Effect(duration, effect, rect, screen))
