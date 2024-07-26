"""This file handles all texture loading and scaling in the game."""

import gif_pygame
import pygame


class Textures:
    """This class provides a support to the game in way of providing textures, scaling them and storing them loaded."""

    def __init__(self, screen):
        self.textures = {}
        self.screen = screen
        self.textures["screen"] = screen
        self.load_textures()

    def __getitem__(self, index: str) -> pygame.Surface | gif_pygame.GIFPygame:
        return self.textures[index]

    def load_textures(self) -> None:
        """Loads all the textures at the start of the game."""
        self.add_texture("background", self.screen.get_width(), self.screen.get_height())
        self.add_texture("player", 100, 100)
        self.add_texture("enemy", 50, 50)
        self.add_texture("boss_1", 250, 250)
        self.add_texture("boss_2", 250, 250)
        self.add_texture("player_bullet", 40, 40)
        self.add_texture("enemy_bullet", 32, 32)
        self.add_texture("speed", 48, 48)
        self.add_texture("damage", 48, 48)
        self.add_texture("heal", 48, 48)

        self.add_gif("boom_effect")

    def add_texture(self, name: str, size_x=None, size_y=None) -> None:
        """
        This is adding a texture to the dictionary. If size_x and size_y is None then not scaled.
        :param name: Name of texture
        :param size_x: width of texture
        :param size_y: height of texture
        :return: None
        """
        image = pygame.image.load(f"./textures/{name}.png").convert_alpha()
        if size_x is not None and size_y is not None:
            image = pygame.transform.scale(image, (size_x, size_y))
        self.textures[name] = image

    def add_gif(self, name: str) -> None:
        """
        This function loads a gif from a folder.
        :param name: Name of gif
        :return: None
        """
        gif = gif_pygame.load(f"./textures/{name}.gif")
        self.textures[name] = gif
