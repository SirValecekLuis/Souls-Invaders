import pygame


class Sounds:
    def __init__(self):
        self._sounds = dict()

    def __getitem__(self, index: str) -> pygame.mixer.Sound:
        item = self._sounds.get(index)
        if not item:
            sound = pygame.mixer.Sound(f"sounds/{index}.mp3")
            sound.set_volume(0.3)
            self._sounds[index] = sound
            return sound
        return item
