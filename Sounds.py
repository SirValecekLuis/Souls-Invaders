import pygame


class Sounds:
    def __init__(self):
        self.sounds = dict()
        self.load_sounds()

    def __getitem__(self, index: str) -> pygame.mixer.Sound:
        return self.sounds[index]

    def load_sounds(self):
        self.load_wav("shot_sound", 0.3)
        self.load_wav("small_explosion", 0.3)

    def load_wav(self, name: str, volume=0.5):
        self.sounds[name] = pygame.mixer.Sound(f"sounds/{name}.wav")
        self.set_volume(name, volume)

    def load_mp3(self, name: str, volume=0.5):
        self.sounds[name] = pygame.mixer.Sound(f"sounds/{name}.mp3")
        self.set_volume(name, volume)

    def set_volume(self, name: str, volume: float):
        self.sounds[name].set_volume(volume)
