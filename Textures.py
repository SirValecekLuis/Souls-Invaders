import pygame
import gif_pygame


class Textures:
    def __init__(self, screen):
        self.textures = dict()
        self.screen = screen
        self.textures["screen"] = screen
        self.load_textures()

    def __getitem__(self, index: str) -> pygame.Surface | gif_pygame.GIFPygame:
        return self.textures[index]

    def load_textures(self):
        self.add_texture("background", self.screen.get_width(), self.screen.get_height())
        self.add_texture("player", 100, 100)
        self.add_texture("enemy", 50, 50)
        self.add_texture("boss_1", 250, 250)
        self.add_texture("boss_2", 250, 250)
        self.add_texture("player_bullet", 40, 40)
        self.add_texture("enemy_bullet", 40, 40)

        self.add_gif("boom_effect")

    def add_texture(self, name: str, size_x=None, size_y=None):
        image = pygame.image.load(f"textures/{name}.png")
        if size_x is not None and size_y is not None:
            image = pygame.transform.scale(image, (size_x, size_y))
        self.textures[name] = image

    def add_gif(self, name: str):
        gif = gif_pygame.load(f"textures/{name}.gif")
        self.textures[name] = gif
