import pygame
import pygame_menu

from src.managers.screen_manager import ScreenManager
from src.managers.service_manager import ServiceManager
from src.managers.time_manager import TimeManager


class MainMenu:
    def __init__(self):
        self.screen = ServiceManager.get(ScreenManager)
        self.time = ServiceManager.get(TimeManager)
        self.theme = pygame_menu.themes.Theme(
            background_color=(40, 40, 40),
            title_font=pygame.font.Font("./font/OptimusPrinceps.ttf", 70),
            widget_font=pygame.font.Font("./font/OptimusPrinceps.ttf", 45),
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            widget_padding=15,
            selection_color=(129, 0, 1),
        )

        self.menu = pygame_menu.Menu('Souls Invaders', self.screen.get_width(), self.screen.get_height(),
                                     theme=self.theme)

        self.menu.add.button('Play', self.new_game)
        self.menu.add.button('Settings', self.settings)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def new_game(self):
        self.time.toggle_pause()
        self.menu.disable()

    def settings(self):
        ...

    def start(self):
        self.time.toggle_pause()
        self.menu.mainloop(self.screen.get_screen())
