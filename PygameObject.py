import pygame


class PygameObject:
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 speed_x: float,
                 speed_y: float,
                 texture: pygame.Surface,
                 screen: pygame.Surface):
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.texture = texture
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self) -> None:
        self.screen.blit(self.texture, self.rect.topleft)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def move(self) -> bool:
        screen_w, screen_h = pygame.display.get_window_size()

        if self.rect.x + self.rect.width + self.speed_x > screen_w or self.rect.x + self.speed_x < 0:
            return False

        if self.rect.y + self.rect.height + self.speed_y > screen_h or self.rect.y + self.speed_y < 0:
            return False

        self.rect = self.rect.move(self.speed_x, self.speed_y)
        return True
