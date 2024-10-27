"""This file handles showing all the text that is in the game."""
import pygame

from src.managers.screen_manager import ScreenManager
from src.managers.service_manager import ServiceManager
from src.managers.time_manager import TimeManager
from src.objects.ship import Player


class TextManager:
    """This class will deal with all the text that is on the screen."""

    def __init__(self):
        self.font = pygame.font.Font("./font/OptimusPrinceps.ttf", 24)
        self.time_manager = ServiceManager.get(TimeManager)
        self.screen_manager = ServiceManager.get(ScreenManager)

    def render_hp_time(self, player: Player) -> None:
        """
        Shows time and HP of a player each frame.
        :param player: Player
        :return: None
        """

        hours, remainder = divmod(self.time_manager.get_total_time(), 3_600_000)
        minutes, seconds = divmod(remainder, 60_000)
        seconds //= 1000
        hours, minutes, seconds = int(hours), int(minutes), int(seconds)

        time_text = self.font.render(f"Time: {hours}h {minutes}m {seconds}s", True, (255, 0, 0))
        self.screen_manager.blit(time_text, (10, self.screen_manager.get_height() // 2))

        hp_text = self.font.render(f"HP:  {player.hp}", True, (255, 0, 0))
        self.screen_manager.blit(hp_text, (10, self.screen_manager.get_height() // 2 + time_text.get_height()))

    def render_fps(self) -> None:
        """
        Shows current FPS in the top right corner of the screen.
        """
        fps = self.time_manager.get_fps()
        fps_text = self.font.render(f"FPS: {fps}", True, (255, 0, 0))
        fps_rect = fps_text.get_rect()

        fps_rect.topright = (self.screen_manager.get_width() - 10, 10)
        self.screen_manager.blit(fps_text, fps_rect.topleft)

    def get_centered_text(self, text: str, height: float, font: pygame.font) -> tuple[pygame.Surface, pygame.Rect]:
        """
        This returns a centered text based on given height and text width.
        :param text: Text that should be centered
        :param height: Height where text should be
        :param font: Font of text
        :return: Surface and pygame rect where it was created.
        """
        text = font.render(text, True, (129, 0, 1))
        text.blit(text, (10, self.screen_manager.get_height() // 2))
        rect = text.get_rect()
        rect.center = (self.screen_manager.get_width() // 2, height)

        return text, rect
