"""This file handles all the sound loading and getting in the game."""
import pygame


class Sounds:
    """This class is handling all the Sounds and is working like a dictionary that will return loaded sound."""
    def __init__(self):
        self._sounds = {}

    def __getitem__(self, index: str) -> pygame.mixer.Sound:
        item = self._sounds.get(index)
        if not item:
            sound = pygame.mixer.Sound(f"./sounds/{index}.mp3")
            sound.set_volume(0.3)
            self._sounds[index] = sound
            return sound
        return item
