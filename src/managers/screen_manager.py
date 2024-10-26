import pygame
from pygame.constants import FULLSCREEN, DOUBLEBUF  # pylint: disable=no-name-in-module

class ScreenManager:
    def __init__(self):
        icon = pygame.image.load("./icon.png")
        pygame.display.set_icon(icon)

        # Window settings
        flags = FULLSCREEN | DOUBLEBUF
        self.__screen = pygame.display.set_mode((0, 0), flags, vsync=1, display=0)
        pygame.display.set_caption("Souls Invaders")

    def get_width(self) -> int:
        return self.__screen.get_width()

    def get_height(self) -> int:
        return self.__screen.get_height()

    def get_screen(self) -> pygame.Surface:
        return self.__screen

    def blit(self, text: pygame.Surface | pygame.SurfaceType, coord: tuple[int, int]) -> None:
        self.__screen.blit(text, coord)
