import pygame

from Ship import Player


class TextHandler:
    def __init__(self):
        self.font = pygame.font.Font("font/OptimusPrinceps.ttf", 24)

    def show_ingame_text(self,
                         player: Player,
                         start_time: float,
                         screen: pygame.Surface):
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
        text = font.render(text, True, (129, 0, 1))
        text.blit(text, (10, screen.get_height() // 2))
        rect = text.get_rect()
        rect.center = (screen.get_width() // 2, height)

        return text, rect
