import pygame
import gif_pygame
import time


class Effect:
    def __init__(self, duration: float, effect: gif_pygame.GIFPygame, rect: pygame.rect.Rect, screen: pygame.Surface):
        self.effect = effect
        gif_pygame.transform.scale(self.effect, (rect.width, rect.height))
        self.rect = rect
        self.screen = screen
        self.duration = duration
        self.start_time = time.time()

    def update(self) -> bool:
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= self.duration:
            return False

        self.effect.render(self.screen, self.rect)

        return True


class Effects:
    def __init__(self):
        self.effects = []

    def update_all_effects(self):
        for i in range(len(self.effects) - 1, -1, -1):
            effect = self.effects[i]
            if not effect.update():
                self.effects.pop(i)

    def append(self, duration: float, effect: gif_pygame.GIFPygame, rect: pygame.rect.Rect, screen: pygame.Surface):
        self.effects.append(Effect(duration, effect, rect, screen))
