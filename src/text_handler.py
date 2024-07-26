"""This file handles showing all the text that is in the game."""
import pygame

from ship import Player


class TextHandler:
    """This class will deal with all the text that is on the screen."""

    def __init__(self):
        self.font = pygame.font.Font("./font/OptimusPrinceps.ttf", 24)

    def show_ingame_text(self,
                         player: Player,
                         start_time: float,
                         screen: pygame.Surface) -> None:
        """
        Shows time and HP of a player each frame.
        :param player: Player
        :param start_time: Started time since playing
        :param screen: Pygame Screen
        :return: None
        """
        hours, remainder = divmod(pygame.time.get_ticks() - start_time, 3_600_000)
        minutes, seconds = divmod(remainder, 60_000)
        seconds //= 1000

        time_text = self.font.render(f"Time: {hours}h {minutes}m {seconds}s", True, (255, 0, 0))
        screen.blit(time_text, (10, screen.get_height() // 2))

        hp_text = self.font.render(f"HP:  {player.hp}", True, (255, 0, 0))
        screen.blit(hp_text, (10, screen.get_height() // 2 + time_text.get_height()))

    @staticmethod
    def get_centered_text(text: str, height: float, font: pygame.Font, screen: pygame.Surface) -> (
            tuple)[pygame.Surface, pygame.Rect]:
        """
        This returns a centered text based on given height and text width.
        :param text: Text that should be centered
        :param height: Height where text should be
        :param font: Font of text
        :param screen: Pygame screen
        :return: Surface and pygame rect where it was created.
        """
        text = font.render(text, True, (129, 0, 1))
        text.blit(text, (10, screen.get_height() // 2))
        rect = text.get_rect()
        rect.center = (screen.get_width() // 2, height)

        return text, rect
