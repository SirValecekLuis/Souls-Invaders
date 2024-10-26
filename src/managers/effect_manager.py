import pygame
from gif_pygame import gif_pygame

from src.objects.effect import Effect


class EffectManager:
    """Class that handles all effects in the game (gifs)"""

    def __init__(self):
        self.effects = []

    def update_all_effects(self) -> None:
        """This function checks all the effects and """
        for i in range(len(self.effects) - 1, -1, -1):
            effect = self.effects[i]
            if not effect.update():
                self.effects.pop(i)

    def append(self, duration: float, effect: gif_pygame.GIFPygame, rect: pygame.Rect,):
        """If effect is created, then is added in the list, so it can be handled by effects class."""
        self.effects.append(Effect(duration, effect, rect))
