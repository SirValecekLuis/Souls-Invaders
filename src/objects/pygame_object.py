"""
This file is for basic PygameObject class that handles basic stuff like movement and drawing for objects on screen.
"""

import pygame

from src.managers.screen_manager import ScreenManager
from src.managers.service_manager import ServiceManager


class PygameObject:
    """
    This class represents a simple object that will be drawn on screen and is an abstraction that other classes should
    inherit from if they appear on the screen. The class handles basic drawing and moving if any (can be 0 for static)
    """

    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 texture: pygame.Surface | None):

        self.rect = pygame.Rect(x, y, w, h)
        self.screen = ServiceManager.get(ScreenManager)
        if texture:
            self.texture = texture
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self) -> None:
        """
        This function will draw each frame the class that inherited from PygameObject.
        :return: None
        """
        if self.texture is not None:
            self.screen.blit(self.texture, self.rect.topleft)
        else:
            pygame.draw.rect(self.screen.get_screen(), (255, 0, 0), self.rect)

    def move(self) -> bool:
        """
        This function handles moving of a character and respects boundaries of the game
        :return: True if moved, False if move was not possible due to boundaries or any other aspect.
        """
        screen_w, screen_h = pygame.display.get_window_size()

        if self.rect.x + self.rect.width + self.speed_x > screen_w or self.rect.x + self.speed_x < 0:
            return False

        if self.rect.y + self.rect.height + self.speed_y > screen_h or self.rect.y + self.speed_y < 0:
            return False

        self.rect = self.rect.move(self.speed_x, self.speed_y)
        return True
