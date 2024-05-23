import pygame
from Ship import Ship


class TextHandler:
    @staticmethod
    def show_ingame_text(player: Ship,
                         start_time: float,
                         screen: pygame.Surface):
        font = pygame.font.Font("font/OptimusPrinceps.ttf", 24)

        hours, remainder = divmod(pygame.time.get_ticks() - start_time, 3_600_000)
        minutes, seconds = divmod(remainder, 60_000)
        seconds //= 1000

        time_text = font.render(f"Time: {hours}h {minutes}m {seconds}s", True, (255, 0, 0))
        screen.blit(time_text, (10, screen.get_height() // 2))

        hp_text = font.render(f"HP:  {player.hp}", True, (255, 0, 0))
        screen.blit(hp_text, (10, screen.get_height() // 2 + time_text.get_height()))
